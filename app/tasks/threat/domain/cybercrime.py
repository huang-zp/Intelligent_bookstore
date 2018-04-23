import time
from app.engines import db
from app.models import Domain

from app.logger import ContextLogger
from app.tasks.threat.task import Task
from bs4 import BeautifulSoup


class CrawlCybercrime(Task):
    def __init__(self):
        super().__init__('cybercrime 数据爬取')
        self.logger = ContextLogger('threat_domain')

    def run_crawl(self):
        start = time.time()
        domains = []
        url = 'http://cybercrime-tracker.net/ccam.php'
        source = 'cybercrime-tracker.net'
        _info = self.get(url=url)

        if _info is None:
            self.logger.warning("request returned None   "+source)
            return None
        soup = BeautifulSoup(_info, 'lxml')
        table = soup.findChildren('tbody')[2]
        rows = table.findChildren('tr', attrs={'class': 'monitoring'})
        for row in rows:
            date_str = row.findChildren('td')[1].string
            time_obj = time.strptime(date_str, "%d/%m/%Y %H:%M:%S")
            updatetime = time.strftime("%Y-%m-%d", time_obj)
            domain = row.findChildren('td')[2].string
            hashstr = row.findChildren('td')[3].string
            if self.is_ip(domain): continue
            block = [domain, updatetime, source]
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
                for domain, updatetime, source in domains:
                        flag = db.session.query(Domain).filter(Domain.domain == domain, Domain.source == source).first()

                        if flag is None:
                            new_domain = Domain()
                            new_domain.domain = domain
                            new_domain.updatetime = updatetime
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

        self.logger.info("cybercrime 共收集{0}条数据， 新数据{1}条".format(all_count, avail_count))
        self.logger.info("cybercrime 抓取时间{0}，数据遍历时间{1}".format(crawl_time, storage_time))


if __name__ == "__main__":
    freebuf = CrawlCybercrime()
    freebuf.run_crawl()

