from app.tasks.threat.ip import *
from app.tasks import celery_app


@celery_app.task
def run_ip():
    crawl_1 = CrawlCybercrime()
    crawl_2 = CrawlMalwaredomainlist()
    crawl_3 = CrawlZeustracker()
    crawl_4 = CrawlRutgers()
    crawl_5 = CrawlRulez()
    crawl_6 = CrawlMaxmind()
    crawl_7 = CrawlGreensnow()
    crawl_8 = CrawlGithubusercontent()
    crawl_9 = Crawlemergingthreats()
    crawl_10 = CrawlEmergingthreats()
    crawl_11 = CrawlDshield()
    crawl_12 = CrawlDataplane()
    # crawl_13 = CrawlCybersweat()
    crawl_14 = CrawlCinsscore()
    crawl_15 = CrawlBlocklist()
    # crawl_16 = CrawlBadips()
    crawl_17 = CrawlAlienvault()
    crawl_18 = CrawlAbuse()

    crawl_1.run_crawl()
    crawl_2.run_crawl()
    crawl_3.run_crawl()
    crawl_4.run_crawl()
    crawl_5.run_crawl()
    crawl_6.run_crawl()
    crawl_7.run_crawl()
    crawl_8.run_crawl()
    crawl_9.run_crawl()
    crawl_10.run_crawl()
    crawl_11.run_crawl()
    crawl_12.run_crawl()
    # crawl_13.run_crawl()
    crawl_14.run_crawl()
    crawl_15.run_crawl()
    # crawl_16.run_crawl()
    crawl_17.run_crawl()
    crawl_18.run_crawl()


if __name__ == '__main__':
    run_ip()
