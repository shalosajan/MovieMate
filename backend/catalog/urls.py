# backend/catalog/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ContentViewSet
from catalog import views_tmdb

router = DefaultRouter()
router.register(r'contents', ContentViewSet, basename='content')

# Start with router URLs
urlpatterns = router.urls

# TMDB proxy endpoints (public)
urlpatterns += [
    path("tmdb/trending/movies/", views_tmdb.trending_movies),
    path("tmdb/trending/tv/", views_tmdb.trending_tv),
    path("tmdb/popular/movies/", views_tmdb.popular_movies),
    path("tmdb/popular/tv/", views_tmdb.popular_tv),
    path("tmdb/top-rated/movies/", views_tmdb.top_rated_movies),
    path("tmdb/top-rated/tv/", views_tmdb.top_rated_tv),
    path("tmdb/now-playing/", views_tmdb.now_playing_movies),
    path("tmdb/genres/movies/", views_tmdb.movie_genres),
    path("tmdb/genres/tv/", views_tmdb.tv_genres),
]
