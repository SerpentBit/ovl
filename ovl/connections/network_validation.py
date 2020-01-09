from socket import inet_aton, error


def is_static_ip(ip):
    """
    Checks if the given ip is a static ip for FRC
    :param ip: the ip to be checked, a str
    :return: True if the ip is an FRC static ip, False if it isn't
    """
    if not isinstance(ip, str):
        return False
    if len(ip) == 10:
        if ip.startswith('10.') and ip.count('.') == 3:
            return True
    return False


def is_valid_ip(ip):
    """
     checks if the given ip address (string) is a valid ip
    :param ip: the string of the ip to be checked, can be ipv6 and ipv4
    :return: False if invalid, True if valid
    """
    try:
        inet_aton(ip)
        return True
    except error:
        return False
