from app.exceptions import ParamError


class OneOf:
    def __init__(self, choices, desc=''):
        self.choices = choices
        self.desc = desc

    def __call__(self, value):
        if value not in self.choices:
            raise ParamError(self.desc)


def length_validator(length):
    if length < 0 or length > 100:
        raise ParamError('参数错误')
