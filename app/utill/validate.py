import re


def validate_ip4(ip_str):
    sep = ip_str.split('.')
    if len(sep) != 4:
        return False
    for i,x in enumerate(sep):
        try:
            int_x = int(x)
            if int_x < 0 or int_x > 255:
                return False
        except ValueError as e:
            return False
    return True


def validate_ip6(ip_str):
    """
    Validate a hexidecimal IPv6 ip address.
    :param ip_str: String to validate as a hexidecimal IPv6 ip address.
    :type ip_str: str
    :returns: ``True`` if a valid hexidecimal IPv6 ip address,
              ``False`` otherwise.
    :raises: TypeError
    '''
    """
    # :Regex for validating an IPv6 in hex notation
    # _HEX_RE_1 = re.compile(r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$')
    _HEX_RE = re.compile(r'^:{0,1}([0-9a-fA-F]{0,4}:){0,7}[0-9a-fA-F]{0,4}:{0,1}$')
    # _HEX_RE = re.compile(r'^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}:{0,1}$')

    # :Regex for validating an IPv6 in dotted-quad notation
    _DOTTED_QUAD_RE = re.compile(r'^:{0,1}([0-9a-fA-F]{0,4}:){2,6}(\d{1,3}\.){3}\d{1,3}$')
    if _HEX_RE.match(ip_str):
        if ':::' in ip_str:
            return False
        if '::' not in ip_str:
            halves = ip_str.split(':')
            return len(halves) == 8 and halves[0] != '' and halves[-1] != ''
        halves = ip_str.split('::')
        if len(halves) != 2:
            return False
        if halves[0] != '' and halves[0][0] == ':':
            return False
        if halves[-1] != '' and halves[-1][-1] == ':':
            return False
        return True

    if _DOTTED_QUAD_RE.match(ip_str):
        if ':::' in ip_str:
            return False
        if '::' not in ip_str:
            halves = ip_str.split(':')
            return len(halves) == 7 and halves[0] != ''
        halves = ip_str.split('::')
        if len(halves) > 2:
            return False
        hextets = ip_str.split(':')
        quads = hextets[-1].split('.')
        for q in quads:
            if int(q) > 255 or int(q) < 0:
                return False
        return True
    return False


def validate_domain(domain_str):
    _DOMAIN_RE = re.compile(r'(?i)\b((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b')
    if _DOMAIN_RE.match(domain_str):
        return True
    return False


if __name__ == '__main__':

    print(validate_ip4('255.1.1.1'))

    print(validate_ip6('fe80:0000:0000:0000:0204:61ff:254.157.241.86'))

    print(validate_domain('huangzp.com'))
