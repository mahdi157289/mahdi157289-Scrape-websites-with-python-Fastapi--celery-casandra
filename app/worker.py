from celery import Celery
from . import config

celery_app = Celery(__name__)
settings = config.get_settings()

REDIS_URL = settings.redis_url  # Replace with your Redis URL
celery_app.conf.broker_url = REDIS_URL
celery_app.conf.result_backend = REDIS_URL

@celery_app.task(bind=True, name="random_task")
def random_task(name):
    print(f"Hello {name} from Celery!")
    return f"Hello {name} from Celery!"