import requests
from django.conf import settings

TMDB_BASE = "https://api.themoviedb.org/3"


def tmdb_get(path, params=None):
    params = params or {}
    params["api_key"] = settings.TMDB_API_KEY
    params["language"] = "en-US"

    url = f"{TMDB_BASE}{path}"
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


# -------- Public (read-only) helpers --------

def trending_movies():
    return tmdb_get("/trending/movie/week")


def trending_tv():
    return tmdb_get("/trending/tv/week")


def popular_movies():
    return tmdb_get("/movie/popular")


def popular_tv():
    return tmdb_get("/tv/popular")


def top_rated_movies():
    return tmdb_get("/movie/top_rated")


def top_rated_tv():
    return tmdb_get("/tv/top_rated")


def now_playing_movies():
    return tmdb_get("/movie/now_playing")


def movie_genres():
    return tmdb_get("/genre/movie/list")


def tv_genres():
    return tmdb_get("/genre/tv/list")


def movie_details(movie_id):
    return tmdb_get(f"/movie/{movie_id}")


def tv_details(tv_id):
    return tmdb_get(f"/tv/{tv_id}")
