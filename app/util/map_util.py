# encoding: utf-8

import hashlib
import re

from app.model import BlackList


def get_md5(s):
    s = s.encode('utf8')  # if isinstance(s, unicode) else s
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


code_map = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
    'y', 'z', '0', '1', '2', '3', '4', '5',
    '6', '7', '8', '9', 'A', 'B', 'C', 'D',
    'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z'
)


def get_hash_key(long_url):
    hkeys = []
    hex = get_md5(long_url)
    for i in range(0, 4):
        n = int(hex[i * 8:(i + 1) * 8], 16)
        v = []
        e = 0
        for j in range(0, 5):
            x = 0x0000003D & n
            e |= ((0x00000002 & n) >> 1) << j
            v.insert(0, code_map[x])
            n = n >> 6
        e |= n << 5
        v.insert(0, code_map[e & 0x0000003D])
        hkeys.append(''.join(v))
    return hkeys


def match_url(url):
    if re.match(r'^https?:/{2}\w.+$', url):
        return url
    else:
        return 'http://' + url


def change_into_short(url):
    return get_hash_key(url)[0]


def format_url(url):
    if r'://' in url:
        domain = url.split(r'://')[1].split(r'/')[0].split(r':')[0]
    else:
        domain = url.split(r'/')[0].split(r':')[0]
    return domain


def in_black(url):
    domain = format_url(url)
    if BlackList.query.filter_by(black=domain).first():
        return True
    else:
        return False


if __name__ == '__main__':
    print(in_black('www.baud.com:20324/23ed/23'))