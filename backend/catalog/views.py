from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Content, Season, Episode
from .serializers import ContentSerializer, SeasonSerializer, EpisodeSerializer
from .services.tmdb import fetch_tmdb_show_and_create, search_tmdb_by_query


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "owner", None) == request.user


class ContentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Content. All endpoints require authentication.
    """
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Content.objects.filter(owner=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # ---------------------------------------------------
    # GET /api/catalog/contents/{id}/seasons/
    # ---------------------------------------------------
    @action(detail=True, methods=["get"])
    def seasons(self, request, pk=None):
        content = self.get_object()

        if content.owner != request.user:
            return Response(
                {"detail": "Not owner"},
                status=status.HTTP_403_FORBIDDEN,
            )

        seasons = Season.objects.filter(content=content).order_by("season_number")
        serializer = SeasonSerializer(seasons, many=True)
        return Response(serializer.data)

    # ---------------------------------------------------
    # POST /api/catalog/contents/{id}/toggle_episode/
    # ---------------------------------------------------
    @action(detail=True, methods=["post"])
    def toggle_episode(self, request, pk=None):
        content = self.get_object()

        if content.owner != request.user:
            return Response({"detail": "Not owner"}, status=status.HTTP_403_FORBIDDEN)

        season_number = request.data.get("season_number")
        episode_number = request.data.get("episode_number")
        title = request.data.get("title", "")

        if not season_number or not episode_number:
            return Response(
                {"detail": "season_number and episode_number required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        season_number = int(season_number)
        episode_number = int(episode_number)

        season, _ = Season.objects.get_or_create(
            content=content, season_number=season_number
        )

        episode, _ = Episode.objects.get_or_create(
            season=season,
            episode_number=episode_number,
            defaults={"title": title},
        )

        watched = episode.toggle_watched()
        return Response(
            {
                "episode": EpisodeSerializer(episode).data,
                "watched": watched,
            }
        )

    # ---------------------------------------------------
    # POST /api/catalog/contents/{id}/mark_season_watched/
    # ---------------------------------------------------
    @action(detail=True, methods=["post"])
    def mark_season_watched(self, request, pk=None):
        content = self.get_object()

        if content.owner != request.user:
            return Response({"detail": "Not owner"}, status=status.HTTP_403_FORBIDDEN)

        season_number = request.data.get("season_number")
        if not season_number:
            return Response(
                {"detail": "season_number required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        season_number = int(season_number)

        season, _ = Season.objects.get_or_create(
            content=content,
            season_number=season_number,
        )

        if season.episodes_count:
            existing = season.episodes.count()
            for i in range(existing + 1, season.episodes_count + 1):
                Episode.objects.get_or_create(
                    season=season,
                    episode_number=i,
                )

        season.mark_all_watched()
        return Response({"detail": f"Season {season_number} marked watched"})

    # ---------------------------------------------------
    # POST /api/catalog/contents/import_tmdb/
    # ---------------------------------------------------
    @action(
        detail=False,
        methods=["post"],
        url_path="import_tmdb",
        permission_classes=[permissions.IsAuthenticated],
    )
    def import_tmdb(self, request):
        tmdb_id = request.data.get("tmdb_id")
        query = request.data.get("query")

        if not tmdb_id and not query:
            return Response(
                {"detail": "tmdb_id or query required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ prevent duplicate imports
        if tmdb_id:
            existing = Content.objects.filter(
                owner=request.user,
                tmdb_id=str(tmdb_id),
            ).first()

            if existing:
                return Response(
                    ContentSerializer(existing).data,
                    status=status.HTTP_200_OK,
                )

        try:
            content = fetch_tmdb_show_and_create(
                owner=request.user,
                tmdb_id=tmdb_id,
                query=query,
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("IMPORT TMDB ERROR:", e)
            return Response(
                {"detail": "Failed to import title", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            ContentSerializer(content).data,
            status=status.HTTP_201_CREATED,
        )

    # ---------------------------------------------------
    # GET /api/catalog/contents/tmdb_search/?q=...
    # ---------------------------------------------------
    @action(detail=False, methods=["get"])
    def tmdb_search(self, request):
        q = request.query_params.get("q", "")
        if not q:
            return Response(
                {"detail": "q param required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            results = search_tmdb_by_query(q)
        except Exception as e:
            return Response(
                {"detail": "TMDB search failed", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({"results": results})
