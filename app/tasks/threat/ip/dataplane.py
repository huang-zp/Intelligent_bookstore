import time
from app.engines import db
from app.models import IP

from app.logger import ContextLogger
from app.tasks.threat.task import Task


class CrawlDataplane(Task):
    def __init__(self):
        super().__init__('dataplane 数据爬取')
        self.logger = ContextLogger('threat_ip')

    def run_crawl(self):
        start = time.time()
        ips = []
        urls = ['https://dataplane.org/dnsrd.txt',
                'https://dataplane.org/dnsrdany.txt',
                'https://dataplane.org/dnsversion.txt',
                'https://dataplane.org/sipinvitation.txt',
                'https://dataplane.org/sipquery.txt',
                'https://dataplane.org/sipregistration.txt',
                'https://dataplane.org/sshclient.txt',
                'https://dataplane.org/sshpwauth.txt',
                'https://dataplane.org/vncrfb.txt'
                ]
        source = 'dataplane.org'
        for url in urls:
            _info = self.get(url=url)

            if _info is None:
                self.logger.warning("request returned None   " + source)
                return None
            info = _info.split('\n')
            for _ip in info:
                if _ip.startswith('#'): continue
                if _ip == '': continue
                asn = _ip.split('|')[0].strip()
                asname = _ip.split('|')[1].strip()
                ip = _ip.split('|')[2].strip()
                updatetime = _ip.split('|')[3].strip().split()[0]
                category = _ip.split('|')[4].strip()
                block = [ip, updatetime, source, asname, asn, category]
                ips.append(block)
        stop = time.time()
        crawl_time = str(stop - start) + "秒"
        self.save_info(ips, source, crawl_time)

    def save_info(self, ips, source, crawl_time):
        start = time.time()
        all_count = len(ips)
        avail_count = 0
        if len(ips) > 0:
            try:
                for ip, updatetime, source, asname, asn, category in ips:
                    flag = db.session.query(IP).filter(IP.ip == ip, IP.source == source).first()

                    if flag is None:
                        new_ip = IP()
                        new_ip.ip = ip
                        new_ip.updatetime = updatetime
                        new_ip.source = source
                        new_ip.asname = asname
                        new_ip.asn = asn
                        new_ip.category = category
                        db.session.add(new_ip)
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

        self.logger.info("dataplane 共收集{0}条数据， 新数据{1}条".format(all_count, avail_count))
        self.logger.info("dataplane 抓取时间{0}，数据遍历时间{1}".format(crawl_time, storage_time))


if __name__ == "__main__":
    freebuf = CrawlDataplane()
    freebuf.run_crawl()

