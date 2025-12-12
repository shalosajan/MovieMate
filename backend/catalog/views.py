# backend/catalog/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Content, Season, Episode
from .serializers import ContentSerializer, SeasonSerializer, EpisodeSerializer
from .services.tmdb import fetch_tmdb_show_and_create, search_tmdb_by_query

# Custom permission: only owners can modify their Content
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, 'owner', None) == request.user


class ContentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Content. All endpoints require authentication.
    List and create operate on the requesting user's objects.
    """
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Content.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # Toggle an episode's watched flag, creating season/episode if missing
    @action(detail=True, methods=['post'])
    def toggle_episode(self, request, pk=None):
        """
        POST /api/catalog/contents/{id}/toggle_episode/
        payload: { "season_number": 1, "episode_number": 2, "title": "optional title" }
        """
        content = self.get_object()
        # owner check (defensive)
        if content.owner != request.user:
            return Response({'detail': 'Not owner'}, status=status.HTTP_403_FORBIDDEN)

        season_number = request.data.get('season_number')
        episode_number = request.data.get('episode_number')
        ep_title = request.data.get('title', '')

        if not season_number or not episode_number:
            return Response({'detail': 'season_number and episode_number required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            season_number = int(season_number)
            episode_number = int(episode_number)
        except ValueError:
            return Response({'detail': 'season_number and episode_number must be integers'}, status=status.HTTP_400_BAD_REQUEST)

        season, _ = Season.objects.get_or_create(content=content, season_number=season_number)
        episode, created = Episode.objects.get_or_create(season=season, episode_number=episode_number, defaults={'title': ep_title})
        # toggle watched
        new_state = episode.toggle_watched()
        serializer = EpisodeSerializer(episode)
        return Response({'episode': serializer.data, 'watched': new_state}, status=status.HTTP_200_OK)

    # Mark all episodes in a season as watched (create episodes if episodes_count present)
    @action(detail=True, methods=['post'])
    def mark_season_watched(self, request, pk=None):
        """
        POST /api/catalog/contents/{id}/mark_season_watched/
        payload: { "season_number": 1 }
        """
        content = self.get_object()
        if content.owner != request.user:
            return Response({'detail': 'Not owner'}, status=status.HTTP_403_FORBIDDEN)

        season_number = request.data.get('season_number')
        if not season_number:
            return Response({'detail': 'season_number required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            season_number = int(season_number)
        except ValueError:
            return Response({'detail': 'season_number must be integer'}, status=status.HTTP_400_BAD_REQUEST)

        season, created = Season.objects.get_or_create(content=content, season_number=season_number)
        # If episodes_count known, create missing Episode rows
        if season.episodes_count:
            existing = season.episodes.count()
            if existing < season.episodes_count:
                for i in range(existing + 1, season.episodes_count + 1):
                    Episode.objects.get_or_create(season=season, episode_number=i)
        # mark all episodes watched
        season.mark_all_watched()
        return Response({'detail': f'Season {season_number} marked watched'}, status=status.HTTP_200_OK)

    # Import from TMDB (by tmdb_id or by query)
    @action(detail=False, methods=['post'])
    def import_tmdb(self, request):
        """
        POST /api/catalog/contents/import_tmdb/
        payload: { "tmdb_id": 12345 } OR { "query": "Breaking Bad" }
        Returns created Content (owner = request.user)
        """
        tmdb_id = request.data.get('tmdb_id')
        query = request.data.get('query')

        if not tmdb_id and not query:
            return Response({'detail': 'tmdb_id or query required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            created_content = fetch_tmdb_show_and_create(owner=request.user, tmdb_id=tmdb_id, query=query)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            return Response({'detail': 'TMDB import failed', 'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ContentSerializer(created_content, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Optional: search TMDB suggestions (read-only)
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def tmdb_search(self, request):
        """
        GET /api/catalog/contents/tmdb_search/?q=some+title
        Returns TMDB search results (limited)
        """
        q = request.query_params.get('q', '')
        if not q:
            return Response({'detail': 'q param required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            results = search_tmdb_by_query(q)
        except Exception as exc:
            return Response({'detail': 'TMDB search failed', 'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'results': results}, status=status.HTTP_200_OK)
