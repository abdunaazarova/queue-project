# Navbat.uz Queue Management System

## Run locally
1. python -m venv .venv
2. .venv\Scripts\activate
3. pip install -r requirements.txt
4. python manage.py makemigrations
5. python manage.py migrate
6. python manage.py createsuperuser
7. python manage.py seed_data
8. python manage.py runserver

## Railway deployment
- Set environment variables from `.env.example`
- For local development, keep `DEBUG=True` (default). For Railway, set `DEBUG=False`.
- Railway will run `Procfile` commands automatically (`web` + `release`).
- `web` binds Gunicorn to `PORT` and `release` runs migrations + `collectstatic`.
