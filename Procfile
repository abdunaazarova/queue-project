web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn navbat_uz.wsgi:application --bind 0.0.0.0:${PORT:-8000} --log-file -
