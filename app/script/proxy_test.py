# coding: utf-8
import requests


def get_proxy():
    resp =  requests.get("http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=1e9670deaffa43e98917ce23e59ac581&count=1&expiryDate=0&format=1")
    print(resp)
    data = resp.json()

    port = data['msg'][0]['port']
    ip = data['msg'][0]['ip']
    return ip+':'+port


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# your spider code


def getHtml():
    # ....
    retry_count = 5
    proxy = get_proxy()
    while retry_count > 0:
        try:
            html = requests.get('https://book.douban.com/tag/小说?start=740&type=S', proxies={"https": "https://125.105.106.18:20477"})
            # 使用代理访问
            print(html.text)
            if html.status_code != 200:
                delete_proxy(proxy)
                proxy = get_proxy()
                print(str(proxy, encoding = "utf-8"))
                print(html.text)
        except Exception:
            print(Exception)
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    return None

print(get_proxy())