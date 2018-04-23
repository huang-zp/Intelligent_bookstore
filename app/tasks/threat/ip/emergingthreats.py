import re
import time
from datetime import datetime
from app.engines import db
from app.models import IP

from app.logger import ContextLogger
from app.tasks.threat.task import Task


class Crawlemergingthreats(Task):
    def __init__(self):
        super().__init__('emergingthreats 数据爬取')
        self.logger = ContextLogger('threat_ip')

    def run_crawl(self):
        start = time.time()
        ips = []
        url = 'http://rules.emergingthreats.net/open/suricata/rules/botcc.rules'
        source = 'rules.emergingthreats.net'

        _info = self.get(url=url)

        if _info is None:
            self.logger.warning("request returned None   "+source)
            return None
        blocks = re.findall(r'(\[.*\))', _info)
        for block in blocks:
            _ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}', block)
            description = re.search('classtype:(.*?);', block).group(1)
            for ip in _ips:
                block = [ip, description, source]
                ips.append(block)
        stop = time.time()
        crawl_time = str(stop - start) + "秒"
        self.save_info(ips, source, crawl_time)

    def save_info(self, ips, source, crawl_time):
        start = time.time()
        all_count = len(ips)
        avail_count = 0
        _time = datetime.now().strftime("%Y-%m-%d")
        if len(ips) > 0:
            try:
                for ip, description, source in ips:
                    flag = db.session.query(IP).filter(IP.ip == ip, IP.source == source).first()

                    if flag is None:
                        new_ip = IP()
                        new_ip.ip = ip
                        new_ip.description = description
                        new_ip.source = source
                        db.session.add(new_ip)
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

        self.logger.info("emergingthreats 共收集{0}条数据， 新数据{1}条".format(all_count, avail_count))
        self.logger.info("emergingthreats 抓取时间{0}，数据遍历时间{1}".format(crawl_time, storage_time))


if __name__ == "__main__":
    freebuf = Crawlemergingthreats()
    freebuf.run_crawl()

