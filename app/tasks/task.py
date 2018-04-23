import sys
import requests
from app.engines import db
from app.logger import ContextLogger
from app.utill.req import BaseReq


class Task(BaseReq):
    def __init__(self, name, time=None):
        super().__init__()
        self.logger = ContextLogger('task')
        self.name = name
        self.time = time
        self.headers = {
            'Upgrade - Insecure - Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www.baidu.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }
        self.cookies = {}

    def start(self):
        self.logger.info("Task Started: {}".format(self.name))

    def exit(self):
        sys.exit()

    def finish(self):
        self.logger.info("Task Finished: {}".format(self.name))

    def run(self):
        self.start()
        self.run_crawl()
        self.finish()

    def safe_commit(self, value):
        try:
            db.session.add(value)
            db.session.commit()
            self.logger.info(value.title + '提交成功')
        except Exception as e:
            self.logger.warning(e)
            db.session.rollback()







