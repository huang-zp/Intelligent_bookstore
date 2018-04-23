
import json
from app.models import IP
from app.engines import db
from app.tasks import celery_app
from app.utill.req import BaseReq

req = BaseReq()


@celery_app.task
def get_ip_info():

    ips = db.session.query(IP).filter(IP.country == '').all()
    for ip in ips:

        data = req.get('http://ip.taobao.com/service/getIpInfo.php?ip=' + ip.ip)
        data = json.loads(data)
        try:
            data = data['data']
            print(data)
            ip.country = data['country'].replace('XX', '')
            ip.region = data['region'].replace('XX', '')
            ip.city = data['city'].replace('XX', '')
            ip.county = data['county'].replace('XX', '')
            ip.isp = data['isp'].replace('XX', '')
        except Exception as e:
            req.logger.warning(e)
        safe_commit(ip)


def safe_commit(value):
    try:
        db.session.add(value)
        db.session.commit()
        req.logger.info('同步数据：', value.id, ':',  value.ip)
    except Exception as e:
        req.logger.warning(e)
        db.session.rollback()


if __name__ == "__main__":
    get_ip_info()






