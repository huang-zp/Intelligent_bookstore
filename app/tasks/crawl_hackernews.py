from datetime import timedelta, datetime
from app.engines import db
from app.models import Infomation

from app.logger import ContextLogger
from app.tasks.task import Task
from bs4 import BeautifulSoup

now = datetime.now().strftime("%Y-%m-%d")
end_time = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")


class CrawlHackernews(Task):
    def __init__(self):
        super().__init__('hackernews数据爬取')
        self.logger = ContextLogger('task_hackernews')

    def run_crawl(self):
        base_url = 'http://hackernews.cc/page/'
        index = 1
        while index < 275:
            next_page = base_url + str(index)
            html = self.get_one_page(next_page)
            if html:
                result = self.handle_list_html(html)
                if result:
                    break
            index += 1

    def handle_list_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        for article in soup.find(class_="classic-lists clearfix").find_all(id='article'):
            article_url = article.find(class_="classic-list-left").a['href']
            html = self.get_one_page(article_url)
            if html:
                result = self.handle_info_html(html, article_url)
                if result:
                    return result
        return False

    def handle_info_html(self, html, url):
        soup = BeautifulSoup(html, 'lxml')
        try:
            info_url = db.session.query(Infomation).filter_by(url=url).first()
            if info_url:
                return True
            title = soup.find(class_="post-details-right").find(class_="single-title").get_text().strip()
            posted_time = soup.find(class_="post-details-right").find(class_="light-post-meta").find_all('a')[
                1].get_text().strip()
            author = soup.find(class_="post-details-right").find(class_="light-post-meta").find_all('a')[
                0].get_text().strip()
            summary = soup.find(class_="post-body clearfix").find('p').get_text().strip()
            source = 'HackerNews'
            keys = ''
            for category in soup.find(class_="post-details-right").find(class_="light-post-meta").find(
                    class_="post-category").find_all('a'):
                keys = keys + category.get_text().strip() + ';'
        except Exception as e:
            self.logger.warning(url + ' ' + str(e))
            return False
        info = Infomation()
        info.source = source
        info.summary = summary
        info.keys = keys
        info.author = author
        info.posted_time = posted_time
        info.title = title
        info.url = url
        print(info.title, '\n', info.author, '\n', info.posted_time, '\n', info.url, '\n', info.keys, '\n', info.source,
              '\n', info.summary, '\n')
        self.safe_commit(info)
        return False


if __name__ == "__main__":
    freebuf = CrawlHackernews()
    freebuf.run()


