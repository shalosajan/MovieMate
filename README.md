🟦 Backend — MovieMate (Django + DRF)

The MovieMate backend provides APIs for managing a personal movie & TV show collection, including TMDB-powered imports, progress tracking for shows, and user authentication using JWT.

⚙️ Tech Stack

Backend Framework: Django 5 + Django REST Framework

Auth: JWT (SimpleJWT)

Database: SQLite (dev) / PostgreSQL (prod-ready)

External API: TMDB (search, movie/TV metadata)

Environment Management: python-decouple

Testing: Django TestCase + unittest.mock

🚀 Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/shalosajan/MovieMate
cd MovieMate/backend

2️⃣ Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Create your .env file

Copy the example env file:

cp .env.example .env


Then open .env and add your TMDB API key:

SECRET_KEY=your_django_secret
DEBUG=True
TMDB_API_KEY=your_tmdb_key_here


⚠️ .env is ignored by Git to prevent leaking secrets.

5️⃣ Apply migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Create an admin user (optional)
python manage.py createsuperuser

7️⃣ Run the server
python manage.py runserver


Backend will start at:
👉 http://127.0.0.1:8000

🔐 Authentication

JWT authentication is used for all API calls.

Obtain tokens
POST /api/accounts/token/
{
  "username": "john",
  "password": "password"
}


Response:

{
  "access": "...",
  "refresh": "..."
}


Send the access token with every request:

Authorization: Bearer <access_token>

Register
POST /api/accounts/register/

Current user profile
GET /api/accounts/me/
PATCH /api/accounts/me/

🎬 TMDB Integration

MovieMate can import movies or TV shows via TMDB using:

Import by query
POST /api/catalog/contents/import_tmdb/
{
  "query": "Breaking Bad"
}

Import by TMDB ID
POST /api/catalog/contents/import_tmdb/
{
  "tmdb_id": 1396
}

Search TMDB (without creating items)
GET /api/catalog/contents/tmdb_search/?q=Batman

📚 Catalog API
List user content
GET /api/catalog/contents/

Create content manually
POST /api/catalog/contents/

Retrieve / update / delete content
GET /api/catalog/contents/{id}/
PATCH /api/catalog/contents/{id}/
DELETE /api/catalog/contents/{id}/

📺 TV Show Progress Tracking
Toggle an episode watched/unwatched
POST /api/catalog/contents/{id}/toggle_episode/
{
  "season_number": 1,
  "episode_number": 3
}


This automatically:

Creates the season/episode if missing

Toggles its watched flag

Updates content status (watching, completed) intelligently

Mark an entire season as watched
POST /api/catalog/contents/{id}/mark_season_watched/
{
  "season_number": 2
}


If TMDB provided episode counts, missing episodes are auto-created.

⭐ Features Implemented
User Management

Register

Login (JWT)

Profile view/update

Content Management

Add movies & TV shows

Import from TMDB (search or ID)

Season & episode structure auto-generated for TV shows

Progress Tracking

Toggle episode watched state

Mark entire season watched

Auto-update status (wishlist → watching → completed)

Progress % calculation

Filtering

Filtering is done on the frontend using data returned from:

status

type

platform

rating

Cleansed Architecture

accounts app → auth logic

catalog app → content, seasons, episodes

services/tmdb.py → external API integration

serializers.py → structured nested responses

tests/ → mocked tests for TMDB import

🧪 Running Tests

Tests use mocking so they run without calling TMDB.

python manage.py test


Included tests:

TMDB import (TV + movie)

Season creation metadata

Episode creation and watched toggle logic

📁 API Folder Structure (backend)
backend/
│
├── accounts/           # Auth (JWT), register, profile
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── catalog/            # Movies, TV shows, seasons, episodes
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── services/
│   │    └── tmdb.py    # TMDB import logic
│   ├── urls.py
│   └── tests/
│        └── test_tmdb_service.py
│
├── moviemate_project/
│   ├── settings.py
│   └── urls.py
│
└── requirements.txt

💬 Notes for Reviewers

TMDB calls are wrapped with retries and custom headers.

Episodes are created lazily for efficiency.

Season metadata (episode_count) stored from TMDB when available.

Strong validation and owner-based query sets ensure data integrity.

All API endpoints require authentication.