# backend/catalog/services/tmdb.py
import logging
from typing import Optional, List, Dict

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.conf import settings
from django.utils.text import Truncator
from django.core.cache import cache
from catalog.models import Content, Season, Episode

logger = logging.getLogger(__name__)

TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


def _requests_session_with_retries(
    retries: int = 3,
    backoff_factor: float = 0.3,
    status_forcelist: tuple = (500, 502, 503, 504),
) -> requests.Session:
    s = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"])
    )
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


def _get(path: str, params: Optional[dict] = None) -> dict:
    params = params or {}
    api_key = getattr(settings, 'TMDB_API_KEY', None)
    if not api_key:
        raise RuntimeError("TMDB_API_KEY not set in settings (check backend/.env).")
    params['api_key'] = api_key
    url = f"{TMDB_BASE}{path}"

    headers = {
        "User-Agent": "MovieMate/1.0 (+https://your-domain.example)",
        "Accept": "application/json",
    }

    session = _requests_session_with_retries()
    try:
        # NOTE: if you had SSL handshake issues while debugging you can pass verify=False here,
        # but do NOT leave verify=False in production.
        resp = session.get(url, params=params, headers=headers, timeout=10)  # , verify=False
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.SSLError as e:
        logger.exception("SSL error when contacting TMDB")
        raise RuntimeError(f"SSL error contacting TMDB: {e}") from e
    except requests.exceptions.ConnectionError as e:
        logger.exception("Connection error when contacting TMDB")
        raise RuntimeError(f"Connection error contacting TMDB: {e}") from e
    except requests.exceptions.HTTPError as e:
        # include response text to aid debugging (but don't leak in production logs)
        text = getattr(e.response, 'text', '')
        logger.exception("HTTP error from TMDB: %s", text[:500])
        raise RuntimeError(f"TMDB returned HTTP error {e.response.status_code}: {text[:300]}") from e
    except Exception as e:
        logger.exception("Unexpected error when calling TMDB")
        raise RuntimeError(f"Unexpected error when calling TMDB: {e}") from e


def search_tmdb_by_query(query, max_results=10, cache_ttl=3600):
    """
    Search TMDB & cache results for `cache_ttl` seconds (default 1 hour).
    """
    # 1. Check Cache
    cache_key = f"tmdb_search:{query.lower().strip()}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    # 2. If not in cache, fetch from API
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

    # 3. Store in Cache
    cache.set(cache_key, results, cache_ttl)

    return results


def fetch_tv_details(tmdb_id: int) -> dict:
    """
    Fetch full TV details for a given TMDB TV id.
    """
    return _get(f"/tv/{tmdb_id}", params={'append_to_response': 'seasons'})


def fetch_movie_details(tmdb_id: int) -> dict:
    """
    Fetch movie details for a given TMDB movie id.
    """
    return _get(f"/movie/{tmdb_id}")


def fetch_tmdb_show_and_create(owner, tmdb_id: Optional[int] = None, query: Optional[str] = None) -> Content:
    """
    High-level helper:
      - If query provided: search and pick first tv/movie match
      - If tmdb_id provided: attempt TV then movie
      - Create Content with owner and create Season rows (episodes_count when available)
        Episodes are created lazily when user toggles or when marking season watched.
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
    import requests as _requests_mod
    try:
        details = fetch_tv_details(tmdb_id)
        media_type = 'tv'
    except _requests_mod.HTTPError:
        # not a TV, try movie
        try:
            details = fetch_movie_details(tmdb_id)
            media_type = 'movie'
        except _requests_mod.HTTPError as exc:
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
            # skip specials (season 0) to avoid confusion
            if season_number is None or season_number == 0:
                continue
            episodes_count = s.get('episode_count') or None
            Season.objects.get_or_create(
                content=content,
                season_number=season_number,
                defaults={'episodes_count': episodes_count}
            )
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
