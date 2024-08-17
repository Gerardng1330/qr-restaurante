web: gunicorn qr_main.wsgi --log-file - 

web: python manage.py migrate && gunicorn qr_main.wsgi