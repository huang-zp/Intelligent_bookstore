import requests
from app.engines import db
from app.logger import ContextLogger


def get_proxy():
    resp = requests.get(
        "http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=1e9670deaffa43e98917ce23e59ac581&count=1&expiryDate=0&format=1")
    print(resp)
    data = resp.json()

    port = data['msg'][0]['port']
    ip = data['msg'][0]['ip']
    return ip + ':' + port




class BaseReq:
    def __init__(self, is_crawl=True):
        self.ses = db.session
        self.is_crawl = is_crawl
        self.logger = ContextLogger('crawl')
        self.proxy = get_proxy()

    def _request(self, url, method='post', timeout=20, retry=10, **kwargs):
        if kwargs.get('headers'):
            headers = kwargs['headers']
        else:
            headers = {}
        if kwargs.get('cookies'):
            cookies = kwargs['cookies']
        else:
            cookies = {}

        try:
            # resp = requests.request(method, '{}'.format(url), timeout=timeout, headers=headers,
            #                         cookies=cookies, **kwargs)

            resp = requests.request(method, '{}'.format(url), timeout=timeout, headers=headers,
                                            cookies=cookies, proxies={"https": "https://{}".format(self.proxy)}, **kwargs)
        except Exception as e:
            self.logger.warning(e)
            if retry > 0:
                if retry == 5:
                    self.proxy = get_proxy()
                return self._request(url, method, timeout, retry=retry-1, **kwargs)
            else:
                return None
        if resp.status_code != 200 and retry > 0:
            if retry == 5:
                self.proxy=get_proxy()
            return self._request(url, method, timeout, retry=retry-1, **kwargs)
        if self.is_crawl:
            return resp.text
        else:
            try:
                data = resp.json()
            except Exception as e:
                self.logger.warning(e)
                data = None
            return data

    def get(self, url, **kwargs):
        return self._request(url, method='get', **kwargs)

    def post(self, url, **kwargs):
        return self._request(url, method='post', **kwargs)

