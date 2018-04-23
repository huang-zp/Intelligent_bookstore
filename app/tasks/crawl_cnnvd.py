
import json
from datetime import timedelta, datetime

from app.engines import db
from app.models import Vulner
from app.logger import ContextLogger
from app.tasks.task import Task
from bs4 import BeautifulSoup


now = datetime.now().strftime("%Y-%m-%d")
end_time = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")


class CrawlCnnvd(Task):
    def __init__(self):
        super().__init__('cnnvd数据爬取')
        self.logger = ContextLogger('task_cnnvd')

    def get_api_id(self, cnnvd_str):
        str_1, str_2, str_3 = cnnvd_str.split('-')
        if len(str_3) == 3:
            return str_2 + '0' + str_3
        return str_2 + str_3

    def api_affect_product(self, id, name_str):
        data = {
            'cvCveid': id,
            'counts': 5
        }
        json_datas = self.post('http://www.cnnvd.org.cn/web/xxk/getEntity.tag', data=data)
        if json_datas == '' or json_datas is None:
            return name_str
        else:
            json_datas = json.loads(json_datas)
            for json_data in json_datas:
                name_str = name_str + json_data['cpr_product_name'] + ';'
            return name_str

    def api_patchs(self, id, patch_dict):
        data = {
            'cvCveid': id,
            'counts': 5
        }
        json_datas = self.post('http://www.cnnvd.org.cn/web/xxk/getEntity.tag', data=data)
        if json_datas == '' or json_datas is None:
            return patch_dict
        else:
            json_datas = json.loads(json_datas)
            for json_data in json_datas:
                patch_name = json_data['cp_cname']
                patch_url = 'http://www.cnnvd.org.cn' + '/web/xxk/bdxqById.tag?id=' + str(json_data['cp_id'])
                patch_dict[patch_name] = patch_url
            return patch_dict

    def run_crawl(self):
        begin_base_url = 'http://www.cnnvd.org.cn' + '/web/vulnerability/querylist.tag?pageno='
        end_base_url = '&repairLd='
        index = 1
        while index < 10597:
            next_page = begin_base_url + str(index) + end_base_url
            print(next_page)
            html = self.get_one_page(next_page)
            if html:
                result = self.handle_list_html(html)
                if result:
                    break
            index += 1

    def handle_list_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        for url in soup.find(class_='list_list').ul.find_all('li'):
            vul_url = 'http://www.cnnvd.org.cn' + url.div.a['href']

            html = self.get_one_page(vul_url)
            if html:
                result = self.handle_info_html(html, vul_url)
                if result:
                    return result
        return False

    def handle_info_html(self, html, url):
        soup = BeautifulSoup(html, 'lxml')
        try:
            simple_list = []
            title = soup.find(class_="detail_xq w770").find('h2').get_text().strip()
            cnnvd_id = soup.find(class_="detail_xq w770").find('ul').find_all('li')[0].span.get_text().strip().split('：')[1]
            for li in soup.find(class_="detail_xq w770").find('ul').find_all('li')[1:]:
                if li.a:
                    simple_list.append(li.a.get_text().strip())

            # 如果时间超过一个月， 返回True，暂停爬取
            if simple_list[5] < end_time:
                return True

            vulner_source = soup.find(class_="detail_xq w770").find('ul').find_all('li')[-1].span.get_text().strip().split('：')[1]
            list = []
            for div in soup.find(class_="fl w770").find_all(class_='d_ldjj'):
                str_value = ''
                for p in div.find_all('p'):
                    str_value += p.get_text().strip()
                list.append(str_value)
            if list[3] != '暂无':
                str_value = ''
                affect_products = soup.find(class_="fl w770").find_all(class_='d_ldjj')[3].find_all(class_='a_title2')
                for i in affect_products:
                    str_value += i.get_text().strip()+';'
                if len(affect_products) == 5:
                    str_value = self.api_affect_product(self.get_api_id(cnnvd_id), str_value)
                list[3] = str_value
            if list[4] != '暂无':
                patch_dict = {}
                patchs = soup.find(class_="fl w770").find_all(class_='d_ldjj')[4].find_all(class_='a_title2')
                for i in patchs:
                    name = i.get_text().strip()
                    patch_url = 'http://www.cnnvd.org.cn' + i['href']
                    patch_dict[name] = patch_url
                if len(patchs) == 5:
                    patch_dict = self.api_patchs(self.get_api_id(cnnvd_id), patch_dict)
                list[4] = patch_dict
        except Exception as e:
            self.logger.warning(url+'--'+str(e))
            return False

        vul = db.session.query(Vulner).filter_by(cnnvd_id=cnnvd_id).first()
        if vul:
            print("查询成功")
        else:
            print("新数据")
            vul = Vulner()
        vul.title = title
        vul.vulner_source = vulner_source
        vul.cnnvd_id = cnnvd_id
        vul.url = url
        vul.level = simple_list[0]
        vul.cve_id = simple_list[1]
        vul.vulner_type = simple_list[2]
        vul.posted_time = simple_list[3]
        vul.threats_type = simple_list[4]
        vul.update_time = simple_list[5]
        vul.describe = list[0]
        vul.source = 'cnnvd'
        vul.solve_way = list[1]
        vul.refer_link = list[2]
        vul.affect_product = list[3]
        vul.patch = list[4]

        print(vul.title, '\n', vul.update_time, '\n', vul.cve_id, '\n', vul.url, '\n\n')

        self.safe_commit(vul)

        return False


if __name__ == "__main__":

    cnnvd = CrawlCnnvd()
    cnnvd.run()


