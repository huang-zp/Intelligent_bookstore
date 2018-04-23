from app.tasks.crawl_cnnvd import CrawlCnnvd
from app.tasks import celery_app


@celery_app.task
def run_cnnvd():
    cnnvd = CrawlCnnvd()
    cnnvd.run()