from celery import Celery

from core.config import settings

celery = Celery(__name__)
celery.conf.broker_url = f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}'
celery.conf.result_backend = f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}'

