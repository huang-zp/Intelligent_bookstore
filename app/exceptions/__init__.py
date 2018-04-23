class BaseError(Exception):
    def __init__(self, message='', code=400, **kwargs):
        self.code = code
        self.desc = message if message else '参数错误'


class ParamError(BaseError):
    pass


class BizError(BaseError):
    pass


class IntegrityError(BaseError):
    pass


class DBError(BaseError):
    pass


class AuthError(BaseError):
    pass


class ServiceError(BaseError):
    """
    third party service error
    """
    pass


class PrivilegeError(BizError):
    pass


class ResourceNotFound(BizError):
    pass
