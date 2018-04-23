from celery import Celery

celery_app = Celery('celery_task', broker='redis://localhost', backend='redis://localhost')

celery_app.config_from_object('app.config.celery_config')