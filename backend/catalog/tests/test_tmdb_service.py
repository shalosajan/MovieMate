from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
import requests
from catalog.services.tmdb import fetch_tmdb_show_and_create

User = get_user_model()

class TMDBServiceTests(TestCase):
    def setUp(self):
        # Create a dummy user for testing
        self.user = User.objects.create_user(username='tester', password='pass1234')

    @patch('catalog.services.tmdb._get')
    def test_fetch_tv_creates_content_and_seasons(self, mock__get):
        # 1. Simulate a TV details response from TMDB
        mock__get.return_value = {
            "name": "Fake Show",
            "poster_path": "/poster.jpg",
            "overview": "A fake show overview.",
            "seasons": [
                {"season_number": 1, "episode_count": 2},
                {"season_number": 2, "episode_count": 3}
            ]
        }

        # 2. Call the function
        content = fetch_tmdb_show_and_create(owner=self.user, tmdb_id=99999)

        # 3. Assertions (Check if it worked)
        self.assertEqual(content.title, "Fake Show")
        self.assertEqual(content.type, 'tv')
        self.assertEqual(content.seasons.count(), 2)

        # Verify season episode counts were preserved
        s1 = content.seasons.get(season_number=1)
        self.assertEqual(s1.episodes_count, 2)

    @patch('catalog.services.tmdb._get')
    def test_fetch_movie_creates_movie_content(self, mock__get):
        # Simulate fetch_tv_details raising HTTPError so code falls back to movie
        mock__get.side_effect = [
            requests.HTTPError("not a tv"),  # First call (TV) fails
            {   # Second call (Movie) succeeds
                "title": "Fake Movie",
                "poster_path": "/movieposter.jpg",
                "overview": "A fake movie overview."
            }
        ]

        content = fetch_tmdb_show_and_create(owner=self.user, tmdb_id=11111)

        self.assertEqual(content.title, "Fake Movie")
        self.assertEqual(content.type, 'movie')
        self.assertEqual(content.seasons.count(), 0)