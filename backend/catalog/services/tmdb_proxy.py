import requests
from django.conf import settings

TMDB_BASE = "https://api.themoviedb.org/3"

# Use a persistent session with headers for performance
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "MovieMate/1.0 (contact: dev@example.com)",
    "Accept": "application/json",
})


def tmdb_get(path, params=None):
    """
    Helper function to make a GET request to the TMDB API.
    Handles API key, language, status checks, and graceful failure.
    """
    params = params or {}
    params["api_key"] = settings.TMDB_API_KEY
    params["language"] = "en-US"

    url = f"{TMDB_BASE}{path}"

    try:
        # Use the persistent SESSION object
        response = SESSION.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        # 🔒 NEVER crash the app on API failure.
        # Log the error (not shown here, but recommended in a real app)
        # and return a safe, predictable, empty result structure.
        return {
            "results": [],
            "error": "TMDB service unavailable"
        }


# -------- Public (read-only) helpers --------

def trending_movies():
    """Fetches movies trending this week."""
    return tmdb_get("/trending/movie/week")


def trending_tv():
    """Fetches TV shows trending this week."""
    return tmdb_get("/trending/tv/week")


def popular_movies():
    """Fetches popular movies."""
    return tmdb_get("/movie/popular")


def popular_tv():
    """Fetches popular TV shows."""
    return tmdb_get("/tv/popular")


def top_rated_movies():
    """Fetches top rated movies."""
    return tmdb_get("/movie/top_rated")


def top_rated_tv():
    """Fetches top rated TV shows."""
    return tmdb_get("/tv/top_rated")


def now_playing_movies():
    """Fetches movies currently in theaters."""
    return tmdb_get("/movie/now_playing")


def movie_genres():
    """Fetches the list of all movie genres."""
    return tmdb_get("/genre/movie/list")


def tv_genres():
    """Fetches the list of all TV genres."""
    return tmdb_get("/genre/tv/list")


def movie_details(movie_id):
    """Fetches full details for a specific movie ID."""
    return tmdb_get(f"/movie/{movie_id}")


def tv_details(tv_id):
    """Fetches full details for a specific TV show ID."""
    return tmdb_get(f"/tv/{tv_id}")

def search_multi(query):
    """Performs a multi-target search (movies, TV, people) based on a query string."""
    return tmdb_get("/search/multi", params={"query": query})