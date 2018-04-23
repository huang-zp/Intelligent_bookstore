import time
from app.engines import db
from app.models import Domain
from app.logger import ContextLogger
from app.tasks.threat.task import Task


class CrawlNetlab(Task):
    def __init__(self):
        super().__init__('netlab 数据爬取')
        self.logger = ContextLogger('threat_domain')

    def run_crawl(self):
        start = time.time()
        domains = []
        url = 'http://data.netlab.360.com/feeds/dga/dga.txt'
        # url='http://67.209.191.170:81/1.txt'
        source = 'data.netlab.360.com'
        _info = self.get(url=url)
        if _info is None:
            self.logger.warning("request returned None   "+source)
            return None
        info = _info.split('\n')
        for _domain in info:
            if _domain.startswith('#'): continue
            if _domain == '': continue
            domain = _domain.split()[1]
            description = _domain.split()[0]
            updatetime = _domain.split()[2]
            block = [domain, updatetime, description, source]
            domains.append(block)
        stop = time.time()
        crawl_time = str(stop - start) + "秒"
        self.save_info(domains, source, crawl_time)

    def save_info(self, domains, source, crawl_time):

        start = time.time()
        all_count = len(domains)
        avail_count = 0
        if len(domains) > 0:
            try:
                for domain, updatetime, description, source in domains:
                        flag = db.session.query(Domain).filter(Domain.domain == domain, Domain.source == source).first()

                        if flag is None:
                            new_domain = Domain()
                            new_domain.domain = domain
                            new_domain.updatetime = updatetime
                            new_domain.description = description
                            new_domain.source = source
                            db.session.add(new_domain)
                            avail_count += 1
                        else:
                            flag.updatetime = updatetime
                            db.session.add(flag)
                db.session.commit()
            except Exception as e:
                self.logger.warning("Error writing to database" + str(e) + source)
        else:
            self.logger.warning("NO record found from: %s" % source)
        stop = time.time()
        storage_time = str(stop - start) + "秒"

        self.logger.info("netlab 共收集{0}条数据， 新数据{1}条".format(all_count, avail_count))
        self.logger.info("netlab 抓取时间{0}，数据遍历时间{1}".format(crawl_time, storage_time))


if __name__ == "__main__":
    freebuf = CrawlNetlab()
    freebuf.run_crawl()

