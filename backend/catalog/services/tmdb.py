# backend/catalog/services/tmdb.py
import requests
from django.conf import settings
from django.utils.text import Truncator

from catalog.models import Content, Season, Episode

TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


def _get(path, params=None):
    params = params or {}
    api_key = getattr(settings, 'TMDB_API_KEY', None)
    if not api_key:
        raise RuntimeError("TMDB_API_KEY not set in settings")
    params['api_key'] = api_key
    url = f"{TMDB_BASE}{path}"
    # We add a User-Agent header so TMDB knows we are a legitimate app, not a bot
    headers = {
        "User-Agent": "MovieMate/1.0",
        "Accept": "application/json"
    }
    
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()

def search_tmdb_by_query(query, max_results=10):
    """
    Search TMDB multi endpoint and return a small sanitized list of matches.
    """
    data = _get("/search/multi", {'query': query})
    results = []
    for r in data.get('results', [])[:max_results]:
        if r.get('media_type') not in ('tv', 'movie'):
            continue
        results.append({
            'id': r.get('id'),
            'title': r.get('name') or r.get('title'),
            'media_type': r.get('media_type'),
            'overview': Truncator(r.get('overview') or '').chars(300),
            'poster_path': (TMDB_IMAGE_BASE + r['poster_path']) if r.get('poster_path') else None,
            'release_date': r.get('first_air_date') or r.get('release_date')
        })
    return results


def fetch_tv_details(tmdb_id):
    """
    Fetch full TV details for a given TMDB TV id.
    """
    return _get(f"/tv/{tmdb_id}", params={'append_to_response': 'seasons'})

def fetch_movie_details(tmdb_id):
    """
    Fetch movie details for a given TMDB movie id.
    """
    return _get(f"/movie/{tmdb_id}")


def fetch_tmdb_show_and_create(owner, tmdb_id=None, query=None):
    """
    High-level helper:
      - If query provided: search and pick first tv/movie match
      - If tmdb_id provided: attempt TV then movie
      - Create Content with owner and create Season rows (episodes_count when available)
        Do NOT create Episode rows for every episode (that can be done lazily when user toggles)
    """
    if query:
        results = search_tmdb_by_query(query, max_results=5)
        if not results:
            raise ValueError("No TMDB results found for query")
        chosen = results[0]
        tmdb_id = chosen['id']

    if not tmdb_id:
        raise ValueError("tmdb_id is required")

    # Try TV first
    try:
        details = fetch_tv_details(tmdb_id)
        media_type = 'tv'
    except requests.HTTPError:
        # not a TV, try movie
        try:
            details = fetch_movie_details(tmdb_id)
            media_type = 'movie'
        except requests.HTTPError as exc:
            raise ValueError("TMDB: resource not found or error") from exc

    # Build content data
    if media_type == 'tv':
        title = details.get('name') or details.get('original_name') or ''
        poster = (TMDB_IMAGE_BASE + details['poster_path']) if details.get('poster_path') else ''
        overview = details.get('overview') or ''
        content = Content.objects.create(
            owner=owner,
            tmdb_id=str(tmdb_id),
            title=title,
            type='tv',
            poster_path=poster,
            overview=overview
        )
        # create Season records (only metadata; episodes not enumerated)
        for s in details.get('seasons', []):
            season_number = s.get('season_number')
            # skip specials (season 0) optionally
            if season_number is None:
                continue
            episodes_count = s.get('episode_count') or None
            # create season (will be unique_together by model)
            Season.objects.get_or_create(content=content, season_number=season_number, defaults={'episodes_count': episodes_count})
        return content

    else:  # movie
        title = details.get('title') or details.get('original_title') or ''
        poster = (TMDB_IMAGE_BASE + details['poster_path']) if details.get('poster_path') else ''
        overview = details.get('overview') or ''
        content = Content.objects.create(
            owner=owner,
            tmdb_id=str(tmdb_id),
            title=title,
            type='movie',
            poster_path=poster,
            overview=overview
        )
        return content
