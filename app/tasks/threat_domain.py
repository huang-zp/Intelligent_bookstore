from app.tasks.threat.domain import *
from app.tasks import celery_app


@celery_app.task
def run_domain():

    crawl_1 = CrawlZeustracker()
    crawl_2 = CrawlMalwaredomainlist()
    crawl_3 = CrawlMalwaredomainlis()
    crawl_4 = CrawlCybercrime()
    crawl_5 = CrawlRansomwaretracker()
    crawl_6 = CrawlNetlab()
    crawl_7 = CrawlMalwaredomains()
    crawl_8 = CrawlIsc()
    crawl_9 = CrawlBambenekconsulting()

    crawl_1.run_crawl()
    crawl_2.run_crawl()
    crawl_3.run_crawl()
    crawl_4.run_crawl()
    crawl_5.run_crawl()
    crawl_6.run_crawl()
    crawl_7.run_crawl()
    crawl_8.run_crawl()
    crawl_9.run_crawl()


if __name__ == '__main__':
    run_domain()

