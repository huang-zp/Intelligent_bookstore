import os
import time
import json
from datetime import timedelta, datetime
import requests
from app.engines import db
from app.models import BookType, Book, Type
from app.logger import ContextLogger
from app.tasks.task import Task
from bs4 import BeautifulSoup


FILE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/app/resources/' + 'booktype.txt'

tag_list = []
with open(FILE_PATH, 'r') as f:
    for line in f:
        tag_list.append(line.strip())


class CrawlCnnvd(Task):
    def __init__(self):
        super().__init__('douban数据爬取')
        self.logger = ContextLogger('douban')

    def run_crawl(self):
        begin_base_url = 'https://book.douban.com/tag/'
        middle_base_url = '?start='
        end_base_url = '&type=S'

        for tag in tag_list:
            start = 0
            while True:
                page_url = begin_base_url + tag + middle_base_url + str(start) + end_base_url
                print(page_url)
                html = self.get(page_url)

                start += 20
                if html:
                    result = self.handle_list_html(html, tag)
                    if result:
                        break

    def handle_list_html(self, html, tag):
        soup = BeautifulSoup(html, 'lxml')
        items = soup.find_all(class_='subject-item')
        if not items:
            return True
        href_list =[]
        for item in items:
            href = item.div.a['href']
            href_list.append(href)
        for href in href_list:

            html = self.get(href)

            if html:
                result = self.handle_info_html(html, tag)
                if result:
                    continue
        return False

    def handle_info_html(self, html, type_tag):

        soup = BeautifulSoup(html, 'lxml')
        book = Book()

        # type_id = db.session.query(Type).filter_by(title=tag).first().id
        try:
            title = soup.h1.span.get_text()
            info = soup.find(class_='article').find(class_='indent').find(class_='subjectwrap clearfix').find(
                class_='subject clearfix').find(id='info')
            string = info.get_text().strip()
            string = string.replace(' ', '')
            string = string.replace(' ', '')
            string = string.replace('\n', '')
            tag_list = ['出版社:', '出品方:', '副标题:', '原作名:', '译者:', '出版年:', '页数:', '定价:', '装帧:', '丛书:', 'ISBN:']
            value_list = []
            if '作者:' in string:
                string = string.replace('作者:', '')

            flag = 0
            for tag in tag_list:
                if tag in string:
                    value = string.split(tag)[0]
                    value_list.append(value)
                    if flag != 0:
                        for i in range(flag):
                            value_list.append('')
                        flag = 0
                else:
                    flag += 1
                    continue
                string = string.split(tag)[1]
                if tag == 'ISBN:':
                    value_list.append(string)

            author =  value_list[0]
            publisher = value_list[1]
            producer = value_list[2]
            subtitle = value_list[3]
            original_title = value_list[4]
            translator = value_list[5]
            year_of_publisher = value_list[6]
            pages = value_list[7]
            price = value_list[8]
            binding = value_list[9]
            series = value_list[10]
            isbn = value_list[11]

            pic_href = soup.find(class_='article').find(class_='indent').find(class_='subjectwrap clearfix').find(
                class_='subject clearfix').find(id='mainpic').a['href']

            score = soup.find(class_='rating_self clearfix').strong.get_text().strip()

            score_people = soup.find(class_='rating_people').get_text()

            related_info = soup.find(class_='related_info')

            infos = related_info.find_all(class_='indent')[:2]

            content_info = str(infos[0].find(class_='intro')).replace('<div class="intro">', '')
            author_info = str(infos[1].find(class_='intro')).replace('<div class="intro">', '')

            book.title = title
            book.author = author
            book.publisher = publisher
            book.producer = producer
            book.translator = translator
            book.subtitle =subtitle
            book.original_title = original_title
            book.year_of_publisher = year_of_publisher
            book.pages = pages
            book.price = price
            book.binding = binding
            book.series = series
            book.isbn = isbn
            book.score = score
            book.score_people = score_people
            book.type = type_tag
            book.content_info = content_info
            book.author_info = author_info
            book.pic_href = pic_href

            self.safe_commit(book)
        except Exception as e:
            self.logger.warning('爬起失败', e)
            return True
        return False


if __name__ == "__main__":

    cnnvd = CrawlCnnvd()
    cnnvd.run()


