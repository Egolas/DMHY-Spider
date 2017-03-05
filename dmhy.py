import random
import requests
from bs4 import BeautifulSoup
import re

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

    with open('file.txt', 'w', encoding="utf-8") as f:
        f.write(resp.text)

    try:
        soup = BeautifulSoup(resp.content, "lxml")
        return soup
    except Exception as error:
        print(error.args[1])
        return
url = 'https://share.dmhy.org/cms/page/name/programme.html'

soup = get_html_tree(url)

titleInfo = []
titleList = []
dayHead = [r'sunarray',r'monarray',r'tuearray',r'wedarray',r'thuarray',r'friarray',r'satarray']
for a in range(7):
    titleInfo.append(re.findall(r'('+dayHead[a]+r'\.push.*<a href="/topics/list\?keyword=.*;)', soup.get_text()))


for titleOfDay in titleInfo:
    print(titleOfDay)
    for title in titleOfDay:
        titleList.append(re.split(r"','",title))

i = 0
while i< titleList.__len__():
    titleList[i][0] = titleList[i][0][0:titleList[i][0].find('.')+1]
    groupInfo = re.findall(r'<a href=".*?">.*?</a>',titleList[i][3])
    titleList[i][3] = []
    for group in groupInfo:
        titleList[i][3].append(re.match(r'.*href="(.*?)">(.*?)</a>',group).groups())
    titleList[i][4] = titleList[i][4][:titleList[i][4].find("']);")]
    i += 1
