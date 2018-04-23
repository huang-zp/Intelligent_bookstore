import re
from datetime import timedelta, datetime

from app.engines import db
from app.models import Infomation

from app.logger import ContextLogger
from app.tasks.task import Task
from bs4 import BeautifulSoup
now = datetime.now().strftime("%Y-%m-%d")
end_time = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")


class CrawlFreebuf(Task):
    def __init__(self):
        super().__init__('freebuf数据爬取')
        self.logger = ContextLogger('task_freebuf')

    def run_crawl(self):
        base_url = 'http://www.freebuf.com/news/page/'
        index = 1
        while index < 290:
            next_page = base_url + str(index)
            html = self.get_one_page(next_page)
            if html:
                result = self.handle_list_html(html)
                if result:
                    break
            index += 1

    def handle_list_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        for tag_div in soup.find_all("div", class_="news-img"):
            article_url = tag_div.a['href']
            print(article_url)
            html = self.get_one_page(article_url)
            if html:
                result = self.handle_info_html(html, article_url)
                if result:
                    return result
        return False

    def handle_info_html(self, html, url):
        print(url)
        soup = BeautifulSoup(html, 'lxml')
        try:
            url = url
            info_url = db.session.query(Infomation).filter_by(url=url).first()
            if info_url:
                print("已经存在")
                return True
            posted_time = soup.find(class_="property").find(class_="time").get_text().strip()
            title = soup.find(class_="articlecontent").find(class_="title").h2.get_text().strip()
            author = soup.find(class_="property").find(rel="author").get_text().strip()
            keys_list = soup.find(class_="property").find(class_="tags").find_all('a')
            key_str = ''
            for key in keys_list:
                key_str = key_str + key.get_text().strip() + ';'
            summary = ''
            for p_string in soup.find(id="contenttxt").find_all(style=re.compile("color: rgb\(0, 176, 80\);*$")):
                if p_string.get_text() is None:
                    continue
                summary += p_string.get_text().strip()
            if summary == '':
                summary = soup.find(id="contenttxt").find('p').get_text().strip()
        except Exception as e:
            self.logger.warning(url + ' ' + str(e))
            return False
        info = Infomation()
        info.title = title
        info.url = url
        info.posted_time = posted_time
        info.author = author
        info.summary = summary
        info.source = 'Freebuf'
        info.keys = key_str
        print(info.title, info.author, info.posted_time, info.url, key_str)
        self.safe_commit(info)
        return False


if __name__ == "__main__":
    freebuf = CrawlFreebuf()
    freebuf.run()


