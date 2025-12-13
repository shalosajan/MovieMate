# backend/catalog/serializers.py
from rest_framework import serializers
from .models import Content, Season, Episode, Wishlist


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
    content_id = serializers.IntegerField(source="id", read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    seasons = SeasonSerializer(many=True, read_only=True)
    progress_percent = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = [
            'id',
            'content_id',
            'owner',
            'tmdb_id',
            'title',
            'type',
            'poster_path',
            'overview',
            'platform',
            'status',
            'rating',
            'review',
            'seasons',
            'progress_percent',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'content_id',
            'owner',
            'seasons',
            'progress_percent',
            'created_at',
            'updated_at',
        ]

    def get_progress_percent(self, obj):
        try:
            return obj.progress_percent()
        except Exception:
            return None

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"
        read_only_fields = ("user",)
