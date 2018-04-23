from app.tasks.crawl_freebuf import CrawlFreebuf
from app.tasks.crawl_hackernews import CrawlHackernews
from app.tasks import celery_app


@celery_app.task
def run_info():
    hackernews = CrawlHackernews()
    freebuf = CrawlFreebuf()
    freebuf.run()
    hackernews.run()
