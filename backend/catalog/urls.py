# backend/catalog/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ContentViewSet
from catalog import views_tmdb, views_wishlist

router = DefaultRouter()
router.register(r"contents", ContentViewSet, basename="content")

urlpatterns = router.urls + [
    # TMDB proxy (public)
    path("tmdb/trending/movies/", views_tmdb.trending_movies),
    path("tmdb/trending/tv/", views_tmdb.trending_tv),
    path("tmdb/popular/movies/", views_tmdb.popular_movies),
    path("tmdb/popular/tv/", views_tmdb.popular_tv),
    path("tmdb/top-rated/movies/", views_tmdb.top_rated_movies),
    path("tmdb/top-rated/tv/", views_tmdb.top_rated_tv),
    path("tmdb/now-playing/", views_tmdb.now_playing_movies),
    path("tmdb/movie/<int:movie_id>/", views_tmdb.movie_details),
    path("tmdb/tv/<int:tv_id>/", views_tmdb.tv_details),
    path("tmdb/search/", views_tmdb.search_tmdb),

    # Wishlist
    path("wishlist/", views_wishlist.wishlist_list),
    path("wishlist/add/", views_wishlist.wishlist_add),
    path("wishlist/remove/<int:tmdb_id>/", views_wishlist.wishlist_remove),
]
