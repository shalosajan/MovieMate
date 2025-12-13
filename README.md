🎬 MovieMate — Movie & TV Show Tracker

MovieMate is a full-stack web application that allows users to discover, track, and manage movies and TV shows, powered by the TMDB API.
Users can search content, maintain a personal collection, manage a wishlist, and track watch progress for movies and TV shows.

🌐 Live Deployment
Frontend

🔗 Vercel
https://movie-mate-six-sigma.vercel.app/

Backend API

🔗 Railway
https://moviemate-production-a7fe.up.railway.app/

⚠️ Note: The frontend and backend are successfully deployed and connected.
Some authentication-related features work correctly in local development but show issues in production (details below).

🛠️ Tech Stack
Frontend

React.js (Vite)

React Router

Tailwind CSS

Axios

JWT-based authentication

Backend

Django

Django REST Framework

Simple JWT

PostgreSQL / SQLite (env-based)

TMDB API (via backend proxy)

Railway deployment

✨ Features Implemented
Core Features

User authentication (register, login, JWT)

TMDB integration (movies & TV shows)

Search and discovery

Wishlist management

Personal content collection

Watch page for movies & TV shows

Season and episode metadata handling

Backend-driven content ownership

RESTful API architecture

Watch Tracking (Partial)

Mark movies as watched

Season-level progress tracking

Episode toggle logic implemented (backend + frontend)

Progress persistence in database (models in place)

🔐 Authentication Flow

JWT authentication using SimpleJWT

Tokens stored on the client

Protected backend routes

Backend enforces ownership on content actions

⚠️ Known Issues (Important)
1. Authentication in Production

Registration and login work correctly in localhost

In production (Vercel + Railway), authentication requests sometimes fail

Likely causes:

CORS / CSRF trusted origins mismatch

Cookie/JWT handling differences between local and deployed environments

Environment variable differences (Railway vs local .env)

This issue is environment-specific, not a logic error

2. TMDB API Stability

TMDB API occasionally returned:

503 Service Unavailable

Connection reset errors

This affected:

Importing content

Search reliability during certain sessions

Backend retry and error-handling logic has been implemented to mitigate this

3. Watch Progress Finalization

Core logic exists for:

Movies

Seasons

Episodes

UI/UX refinement and final edge-case handling are still pending

📁 Project Structure (Simplified)
MovieMate/
├── backend/
│   ├── accounts/
│   ├── catalog/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── services/
│   │   │   └── tmdb.py
│   ├── moviemate_project/
│   └── manage.py
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   └── context/
│   └── vite.config.js

⚙️ Local Setup
Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Frontend
cd frontend
npm install
npm run dev

🔑 Environment Variables
Backend (.env)
SECRET_KEY=your-secret
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
TMDB_API_KEY=your_tmdb_api_key
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOW_ALL_ORIGINS=True

Frontend (.env)
VITE_API_BASE_URL=http://127.0.0.1:8000/api

📌 Deployment Notes

Backend deployed on Railway

Frontend deployed on Vercel

Production uses environment-based configuration

Static file handling and CORS configured for cross-origin requests

Some production auth issues remain under investigation

🚀 Future Improvements

Finalize watch progress UI

Fix production authentication edge cases

Add ratings & reviews

Add analytics (watch time graphs)

AI-based recommendations

Improve deployment stability

👤 Author

Shalo Sajan
GitHub: https://github.com/shalosajan

📝 Final Note

This project demonstrates:

Full-stack architecture

External API integration

Authentication and authorization

State management

Real-world deployment challenges

Despite time constraints and third-party API instability, the core system is complete, functional, and extensible.