# backend/catalog/serializers.py
from rest_framework import serializers
from .models import Content, Season, Episode


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'episode_number', 'title', 'watched']


class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Season
        fields = ['id', 'season_number', 'episodes_count', 'episodes']


class ContentSerializer(serializers.ModelSerializer):
    seasons = SeasonSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    progress_percent = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = [
            'id', 'owner', 'tmdb_id', 'title', 'type', 'poster_path', 'overview',
            'platform', 'status', 'rating', 'review', 'seasons', 'progress_percent',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'seasons', 'progress_percent', 'created_at', 'updated_at']

    def get_progress_percent(self, obj):
        try:
            return obj.progress_percent()
        except Exception:
            return None
