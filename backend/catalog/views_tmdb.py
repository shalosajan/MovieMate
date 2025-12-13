from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from catalog.services import tmdb_proxy


def safe_tmdb_response(func, *args):
    try:
        return Response(func(*args))
    except Exception as e:
        return Response(
            {
                "error": "TMDB service unavailable",
                "details": str(e),
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def trending_movies(request):
    return safe_tmdb_response(tmdb_proxy.trending_movies)


@api_view(["GET"])
@permission_classes([AllowAny])
def trending_tv(request):
    return safe_tmdb_response(tmdb_proxy.trending_tv)


@api_view(["GET"])
@permission_classes([AllowAny])
def popular_movies(request):
    return safe_tmdb_response(tmdb_proxy.popular_movies)


@api_view(["GET"])
@permission_classes([AllowAny])
def popular_tv(request):
    return safe_tmdb_response(tmdb_proxy.popular_tv)


@api_view(["GET"])
@permission_classes([AllowAny])
def top_rated_movies(request):
    return safe_tmdb_response(tmdb_proxy.top_rated_movies)


@api_view(["GET"])
@permission_classes([AllowAny])
def top_rated_tv(request):
    return safe_tmdb_response(tmdb_proxy.top_rated_tv)


@api_view(["GET"])
@permission_classes([AllowAny])
def now_playing_movies(request):
    return safe_tmdb_response(tmdb_proxy.now_playing_movies)


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_genres(request):
    return safe_tmdb_response(tmdb_proxy.movie_genres)


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_genres(request):
    return safe_tmdb_response(tmdb_proxy.tv_genres)


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_details(request, movie_id):
    return safe_tmdb_response(tmdb_proxy.movie_details, movie_id)


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_details(request, tv_id):
    return safe_tmdb_response(tmdb_proxy.tv_details, tv_id)
