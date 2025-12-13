import logging
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from django.conf import settings
from django.utils.text import Truncator
from django.core.cache import cache

from catalog.models import Content, Season

logger = logging.getLogger(__name__)

TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


# -------------------------------------------------------------------
# HTTP SESSION WITH RETRIES
# -------------------------------------------------------------------

def _requests_session_with_retries(
    retries: int = 3,
    backoff_factor: float = 0.3,
    status_forcelist: tuple = (500, 502, 503, 504),
) -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(["GET"])
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


# -------------------------------------------------------------------
# LOW-LEVEL TMDB GET
# -------------------------------------------------------------------

def _get(path: str, params: Optional[dict] = None) -> dict:
    params = params or {}

    api_key = getattr(settings, "TMDB_API_KEY", None)
    if not api_key:
        raise RuntimeError("TMDB_API_KEY not set")

    params["api_key"] = api_key

    session = _requests_session_with_retries()
    url = f"{TMDB_BASE}{path}"

    try:
        resp = session.get(
            url,
            params=params,
            headers={
                "User-Agent": "MovieMate/1.0",
                "Accept": "application/json",
            },
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.exception("TMDB request failed")
        raise RuntimeError(f"TMDB request failed: {e}") from e


# -------------------------------------------------------------------
# SEARCH
# -------------------------------------------------------------------

def search_tmdb_by_query(query, max_results=10, cache_ttl=3600):
    cache_key = f"tmdb_search:{query.lower().strip()}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    data = _get("/search/multi", {"query": query})

    results = []
    for r in data.get("results", [])[:max_results]:
        if r.get("media_type") not in ("movie", "tv"):
            continue

        results.append({
            "id": r["id"],
            "media_type": r["media_type"],
            "title": r.get("title") or r.get("name"),
            "overview": Truncator(r.get("overview") or "").chars(300),
            "poster_path": (
                TMDB_IMAGE_BASE + r["poster_path"]
                if r.get("poster_path")
                else None
            ),
        })

    cache.set(cache_key, results, cache_ttl)
    return results


# -------------------------------------------------------------------
# TMDB DETAIL FETCHERS
# -------------------------------------------------------------------

def fetch_movie_details(tmdb_id: int) -> dict:
    return _get(f"/movie/{tmdb_id}")


def fetch_tv_details(tmdb_id: int) -> dict:
    return _get(f"/tv/{tmdb_id}")


# -------------------------------------------------------------------
# MAIN IMPORT FUNCTION (FIXED)
# -------------------------------------------------------------------

def fetch_tmdb_show_and_create(
    owner,
    tmdb_id: Optional[int] = None,
    query: Optional[str] = None,
) -> Content:
    """
    SAFE, IDEMPOTENT IMPORT
    - Never crashes on duplicates
    - Correctly handles movie vs TV
    """

    # -------------------------------------------------
    # Resolve tmdb_id from query
    # -------------------------------------------------
    if query and not tmdb_id:
        results = search_tmdb_by_query(query, max_results=1)
        if not results:
            raise ValueError("No TMDB results found")
        tmdb_id = results[0]["id"]

    if not tmdb_id:
        raise ValueError("tmdb_id is required")

    # -------------------------------------------------
    # Return existing content if already imported
    # -------------------------------------------------
    existing = Content.objects.filter(
        owner=owner,
        tmdb_id=str(tmdb_id),
    ).first()

    if existing:
        return existing

    # -------------------------------------------------
    # Detect MEDIA TYPE PROPERLY
    # -------------------------------------------------
    try:
        details = fetch_movie_details(tmdb_id)
        media_type = "movie"
    except Exception:
        details = fetch_tv_details(tmdb_id)
        media_type = "tv"

    # -------------------------------------------------
    # CREATE CONTENT
    # -------------------------------------------------
    if media_type == "movie":
        content = Content.objects.create(
            owner=owner,
            tmdb_id=str(tmdb_id),
            type="movie",
            title=details.get("title") or details.get("original_title") or "",
            overview=details.get("overview") or "",
            poster_path=(
                TMDB_IMAGE_BASE + details["poster_path"]
                if details.get("poster_path")
                else ""
            ),
            status="wishlist",
        )
        return content

    # -------------------------------------------------
    # TV SHOW
    # -------------------------------------------------
    content = Content.objects.create(
        owner=owner,
        tmdb_id=str(tmdb_id),
        type="tv",
        title=details.get("name") or details.get("original_name") or "",
        overview=details.get("overview") or "",
        poster_path=(
            TMDB_IMAGE_BASE + details["poster_path"]
            if details.get("poster_path")
            else ""
        ),
        status="wishlist",
    )

    # Create seasons (NO episodes yet)
    for s in details.get("seasons", []):
        season_number = s.get("season_number")

        # ❌ Skip specials
        if season_number in (None, 0):
            continue

        Season.objects.get_or_create(
            content=content,
            season_number=season_number,
            defaults={
                "episodes_count": s.get("episode_count") or 0
            },
        )

    return content
