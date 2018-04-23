import re
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
        self.header = {
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:52.0) Gecko/20100101'
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

    def get_one_page(self, url):
        """
        Crawl a url and return the HTML code for this url.

        Args:
            url: The url you need to crawl.

        Returns:
            the HTML code for this url
        """
        # try:
        #     response = requests.get(url, headers=self.headers)
        # except Exception as e:
        #     self.logger.warning(url + ' ' + str(e))
        #     return False
        # return response.text
        response = self.get(url)
        return response

    def run_crawl(self):
        """
        Traverse all the pages you need to crawl.
        """
        pass

    def handle_list_html(self, html):
        """
        The analysis page gets all the urls you need to crawl.

        Args:
            html: The page HTML that needs to be analyzed
        """
        pass

    def handle_info_html(self, html, url):
        """
        The analysis page extracts all vulnerability information and commit to database.

        Args:
            html: The page HTML that needs to be analyzed
            url: The page url that needs to be analyzed
        """
        pass

    def is_ip(self, _str):
        p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if p.match(_str):
            return True
        else:
            return False

