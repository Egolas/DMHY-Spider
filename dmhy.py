import random

import requests
from bs4 import BeautifulSoup
import re
from pixivspider import *

"""
初步设想：
1、获取所有番剧
2、选择需要自动下载更新的番剧
3、可存储设置
"""


def get_response(url, try_time=1000, **kwargs):
    if 'session' in kwargs:
        s = kwargs.pop('session')
    else:
        s = requests.Session()
    r = None
    while try_time > 0:
        try:
            r = s.get(url, **kwargs)
            break
        except requests.exceptions.RequestException:
            try_time -= 1
    if try_time <= 0:
        try:
            s.get(url, **kwargs)
        except requests.exceptions.RequestException as error:
            raise Exception(error, "过多的尝试")
    return r, s

heads = [{"Accept-Language": "zh-CN,zh;q=0.8",
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240'},
             {"Accept-Language": "zh-CN,zh;q=0.8",
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'},
             {"Accept-Language": "zh-CN,zh;q=0.8",
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'},
             {"Accept-Language": "zh-CN,zh;q=0.8",
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.31'},
             {"Accept-Language": "zh-CN,zh;q=0.8",
              'User-Agent': 'Opera/9.80 (Windows NT 6.1) Presto/2.12.388 Version/12.16'},
             {"Accept-Language": "zh-CN,zh;q=0.8",
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'}]


def get_html_tree( url, header=None, params=None):
    if header is None:
        header = heads[random.randint(0, len(heads) - 1)]
    resp, s = get_response(url, params=params, headers=header, cookies={}, timeout=50)
    try:
        soup = BeautifulSoup(resp.content, "lxml")
        return soup
    except Exception as error:
        print(error)
        return
url = 'https://share.dmhy.org/cms/page/name/programme.html'

try:
    soup = get_html_tree(url)
except Exception as e:
    print(e.args[1])
    exit()

titleList = []
dayHead = [r'sunarray',r'monarray',r'tuearray',r'wedarray',r'thuarray',r'friarray',r'satarray']
for a in range(7):
    titleList.append(re.findall(r'('+dayHead[a]+r'\.push.*<a href="/topics/list\?keyword=.*;)', soup.get_text()))


for a in titleList:
    print(a)

#print(soup.prettify())
"""
for link in soup.find_all("a", href=re.compile("keyword=")):
    print(link)

"""
"""
with open('file.html','wb') as f:
    f.write(response.content)

"""