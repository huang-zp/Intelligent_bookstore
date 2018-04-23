import requests

from app.exceptions import DBError
from app.exceptions import ServiceError
from app.engines import db


class BaseService:

    def __init__(self, server, auth_code, auth_token, need_auth=True):
        self.ses = db.session
        self.need_auth = need_auth
        self.server = server
        self.auth_code = auth_code
        self.auth_token = auth_token

    def _request(self, url, method='post', timeout=10, retry=1, auth=True, **kwargs):
        if not self.server:
            raise ServiceError('服务未配置')
        if kwargs.get('headers'):
            headers = kwargs['headers']
            del(kwargs['headers'])
        else:
            headers = {}
        if auth:
            if not self.auth_token:
                self.refresh_token()
            headers.update({'Authorization': 'Bearer {}'.format(self.auth_token)})
        try:
            resp = requests.request(method, '{}{}'.format(self.server, url), timeout=timeout, headers=headers,
                                    **kwargs)
        except Exception as e:
            raise ServiceError(e)
        if resp.status_code != 200:
            if resp.status_code == 401:
                self.refresh_token()
                return self._request(url, method, timeout, retry=retry-1, **kwargs)
            raise ServiceError('response error: {}, {}'.format(resp.status_code, resp.text))
        try:
            data = resp.json()
        except Exception as e:
            raise ServiceError('response format error: {}'.format(e))
        if data.get('code') == 401 and auth and retry > 0:
            self.refresh_token()
            return self._request(url, method, timeout, retry=retry-1, **kwargs)
        return data

    def get(self, url, **kwargs):
        return self._request(url, method='get', **kwargs)

    def post(self, url, **kwargs):
        return self._request(url, method='post', **kwargs)

    def refresh_token(self):
        pass

    def safe_commit(self):
        try:
            self.ses.commit()
        except Exception as e:
            self.ses.rollback()
            raise DBError(e)
        return True
