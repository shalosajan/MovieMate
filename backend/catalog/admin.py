from django.contrib import admin
from .models import Content, Season, Episode


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'owner', 'status', 'created_at')
    list_filter = ('type', 'status', 'platform', 'owner')
    search_fields = ('title', 'tmdb_id', 'overview', 'owner__username')
    ordering = ('-created_at',)


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('content', 'season_number', 'episodes_count')
    list_filter = ('content',)
    ordering = ('content', 'season_number')


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('season', 'episode_number', 'watched')
    list_filter = ('season__content', 'season')
    search_fields = ('season__content__title',)
    ordering = ('season', 'episode_number')
