# MovieMate

Mini full-stack app to track movies & TV shows (Django backend).

## Quick start (backend)

1. Copy `.env.example` to `backend/.env` and edit secrets.
2. Create virtualenv:
    python -m venv .venv
    source .venv/bin/activate
    pip install -r backend/requirements.txt
3. Run migrations:
    cd backend
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
