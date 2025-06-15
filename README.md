## STACK
* Django Rest Framework
* MySQL
* Redis
* Celery

## START INSTRUCTIONS
1. Install dependencies:
   ```bash
   pip install africastalking celery redis django djangorestframework django_celery_results dotenv django together
   ```
2. Create a `.env` file in the root directory and set the following environment variables:
   ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    celery -A djangoProject worker --loglevel=info
    python manage.py runserver 
    python manage.py migrate     
    ngrok http 8000
   ```