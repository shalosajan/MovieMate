from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from catalog.services import tmdb_proxy


@api_view(["GET"])
@permission_classes([AllowAny])
def trending_movies(request):
    return Response(tmdb_proxy.trending_movies())


@api_view(["GET"])
@permission_classes([AllowAny])
def trending_tv(request):
    return Response(tmdb_proxy.trending_tv())


@api_view(["GET"])
@permission_classes([AllowAny])
def popular_movies(request):
    return Response(tmdb_proxy.popular_movies())


@api_view(["GET"])
@permission_classes([AllowAny])
def popular_tv(request):
    return Response(tmdb_proxy.popular_tv())


@api_view(["GET"])
@permission_classes([AllowAny])
def top_rated_movies(request):
    return Response(tmdb_proxy.top_rated_movies())


@api_view(["GET"])
@permission_classes([AllowAny])
def top_rated_tv(request):
    return Response(tmdb_proxy.top_rated_tv())


@api_view(["GET"])
@permission_classes([AllowAny])
def now_playing_movies(request):
    return Response(tmdb_proxy.now_playing_movies())


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_genres(request):
    return Response(tmdb_proxy.movie_genres())


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_genres(request):
    return Response(tmdb_proxy.tv_genres())
