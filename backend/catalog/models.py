from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Content(models.Model):
    """
    A Content record is a user-owned entry representing either a Movie or a TV Show.
    Use tmdb_id to store the TMDB identifier (optional).
    """
    TYPE_CHOICES = (('movie', 'Movie'), ('tv', 'TV Show'))
    STATUS_CHOICES = (('watching', 'Watching'), ('completed', 'Completed'), ('wishlist', 'Wishlist'))

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contents')
    tmdb_id = models.CharField(max_length=64, blank=True, null=True)
    title = models.CharField(max_length=512)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES, default='movie')
    poster_path = models.URLField(blank=True, null=True)
    overview = models.TextField(blank=True)
    platform = models.CharField(max_length=128, blank=True)  # e.g., Netflix
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='wishlist')
    rating = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    review = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('owner', 'tmdb_id', 'title')  # tmdb_id may be null - title+owner helps avoid duplicates

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"

    # --- Convenience / aggregate methods ---

    def total_episodes(self):
        """
        Returns total episodes across all seasons if season.episodes_count available,
        otherwise returns None when counts are unknown.
        """
        seasons = self.seasons.all()
        if not seasons.exists():
            return None
        total = 0
        known = False
        for s in seasons:
            if s.episodes_count is None:
                return None  # if any season count unknown, return None (we prefer explicit counts)
            total += s.episodes_count
            known = True
        return total if known else None

    def watched_episodes_count(self):
        """
        Count of episodes marked watched (Episode.watched=True).
        """
        return Episode.objects.filter(season__content=self, watched=True).count()

    def progress_percent(self):
        """
        Returns integer percentage of episodes watched across show (0-100) or None if total unknown or not a TV show.
        """
        if self.type != 'tv':
            return None
        total = self.total_episodes()
        if not total:
            return None
        watched = self.watched_episodes_count()
        return min(100, int((watched / total) * 100)) if total > 0 else None

    def update_status_if_needed(self):
        """
        Apply simple business rule:
          - if any episode watched and status == 'wishlist' -> set to 'watching'
          - if all episodes watched and total known -> set to 'completed'
        Call this after toggling episodes or marking season watched.
        """
        if self.type != 'tv':
            return
        total = self.total_episodes()
        watched = self.watched_episodes_count()
        if total is None:
            # If total unknown, only change wishlist->watching when watched > 0
            if watched > 0 and self.status == 'wishlist':
                self.status = 'watching'
                self.save(update_fields=['status'])
            return

        # when total known
        if watched >= total and total > 0:
            if self.status != 'completed':
                self.status = 'completed'
                self.save(update_fields=['status'])
        elif watched > 0 and self.status == 'wishlist':
            self.status = 'watching'
            self.save(update_fields=['status'])


class Season(models.Model):
    """
    A Season belongs to a Content (tv show). episodes_count is optional; if unknown keep null.
    """
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='seasons')
    season_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    episodes_count = models.PositiveIntegerField(null=True, blank=True)  # optional

    class Meta:
        unique_together = ('content', 'season_number')
        ordering = ['season_number']

    def __str__(self):
        return f"{self.content.title} - S{self.season_number}"

    def watched_count(self):
        return self.episodes.filter(watched=True).count()

    def mark_all_watched(self):
        """
        Mark all episodes in this season as watched. Create Episode rows if episodes_count set and episodes missing.
        """
        # If episodes_count is known, ensure Episode rows exist
        if self.episodes_count:
            existing = self.episodes.count()
            if existing < self.episodes_count:
                # create missing episodes
                for i in range(existing + 1, self.episodes_count + 1):
                    Episode.objects.get_or_create(season=self, episode_number=i)
        # mark all existing episodes watched
        self.episodes.update(watched=True)
        # propagate to parent content
        self.content.update_status_if_needed()


class Episode(models.Model):
    """
    Episode is the atomic watchable unit and holds a watched flag.
    Episodes are created on TMDB import (optional) or lazily when user toggles an episode.
    """
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    episode_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    title = models.CharField(max_length=512, blank=True)
    watched = models.BooleanField(default=False)

    class Meta:
        unique_together = ('season', 'episode_number')
        ordering = ['episode_number']

    def __str__(self):
        s_num = self.season.season_number
        return f"{self.season.content.title} S{s_num:02d}E{self.episode_number:02d}"

    def toggle_watched(self):
        """
        Toggle watched flag and update parent content status per rules.
        """
        self.watched = not self.watched
        self.save(update_fields=['watched'])
        # propagate to parent content
        self.season.content.update_status_if_needed()
        return self.watched
