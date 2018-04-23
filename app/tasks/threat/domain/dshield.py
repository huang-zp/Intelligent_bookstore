import time
from datetime import datetime
from app.engines import db
from app.models import Domain

from app.logger import ContextLogger
from app.tasks.threat.task import Task
from urllib.parse import urlparse


class CrawlMalwaredomainlist(Task):
    def __init__(self):
        super().__init__('dshield 数据爬取')
        self.logger = ContextLogger('threat_domain')

    def run_crawl(self):
        start = time.time()
        domains = []
        urls = ['https://secure.dshield.org/feeds/suspiciousdomains_High.txt',
                'https://secure.dshield.org/feeds/suspiciousdomains_Medium.txt',
                'https://secure.dshield.org/feeds/suspiciousdomains_Low.txt'
                ]
        source = 'secure.dshield.org'
        for url in urls:

            obj = urlparse(url)
            description = obj.path.split('/')[-1].split('.')[0]
            _info = self.get(url=url)
            if _info is None:
                self.logger.warning("request returned None   " + source)
                return None
            info = _info.split('\n')
            for domain in info:
                if domain.startswith('#'): continue
                if domain == 'Site': continue
                block = [domain, source, description]
                domains.append(block)
        stop = time.time()
        crawl_time = str(stop - start) + "秒"
        self.save_info(domains, source, crawl_time)

    def save_info(self, domains, source, crawl_time):

        start = time.time()
        all_count = len(domains)
        avail_count = 0
        _time = datetime.now().strftime("%Y-%m-%d")
        if len(domains) > 0:
            try:
                for domain, source, description in domains:
                        flag = db.session.query(Domain).filter(Domain.domain == domain, Domain.source == source).first()

                        if flag is None:
                            new_domain = Domain()
                            new_domain.domain = domain
                            new_domain.source = source
                            new_domain.description = description
                            db.session.add(new_domain)
                            avail_count += 1
                        else:
                            flag.updatetime = _time
                            db.session.add(flag)
                db.session.commit()
            except Exception as e:
                self.logger.warning("Error writing to database" + str(e) + source)
        else:
            self.logger.warning("NO record found from: %s" % source)
        stop = time.time()
        storage_time = str(stop - start) + "秒"

        self.logger.info("dshield 共收集{0}条数据， 新数据{1}条".format(all_count, avail_count))
        self.logger.info("dshield 抓取时间{0}，数据遍历时间{1}".format(crawl_time, storage_time))


if __name__ == "__main__":
    freebuf = CrawlMalwaredomainlist()
    freebuf.run_crawl()

