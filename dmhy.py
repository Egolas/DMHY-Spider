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

class DMHYDailySpider:
    dayHead = [r'sunarray', r'monarray', r'tuearray', r'wedarray', r'thuarray', r'friarray', r'satarray']
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

    def __init__(self,url):
        self.url = url
        self.titleInfo = []
        self.titleList = []
        self.soup = self.get_html_tree(url)

    def get_response(self, url, try_time=1000, **kwargs):
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

    def get_html_tree(self, url, header=None, params=None):
        if header is None:
            header = self.heads[random.randint(0, len(self.heads) - 1)]

        try:
            resp, s = self.get_response(url, params=params, headers=header, cookies={}, timeout=50)
        except Exception as error:
            print(error.args[1])
            exit()

        with open('file.txt', 'w', encoding="utf-8") as f:
            f.write(resp.text)

        try:
            soup = BeautifulSoup(resp.content, "lxml")
            return soup
        except Exception as error:
            print(error)
            return

    def get_base_data(self):
        for a in range(7):
            self.titleInfo.append(re.findall(r'(' + self.dayHead[a] + r'\.push.*<a href="/topics/list\?keyword=.*;)',
                                        dmhySpider.soup.get_text()))

        for titleOfDay in self.titleInfo:
            #print(titleOfDay)
            for title in titleOfDay:
                self.titleList.append(re.split(r"','", title))

        i = 0
        while i < self.titleList.__len__():
            self.titleList[i][0] = self.titleList[i][0][0:self.titleList[i][0].find('.') + 1]
            groupInfo = re.findall(r'<a href=".*?">.*?</a>', self.titleList[i][3])
            self.titleList[i][3] = []
            for group in groupInfo:
                self.titleList[i][3].append(re.match(r'.*href="(.*?)">(.*?)</a>', group).groups())
                self.titleList[i][4] = self.titleList[i][4][:self.titleList[i][4].find("']);")]
            i += 1

        return self.titleList

class TitleGetter:
    titleList = []
    def __init__(self, titleList):
        self.titleList = titleList

    def get_titleList(self):
        return self.titleList






url = 'https://share.dmhy.org/cms/page/name/programme.html'

dmhySpider = DMHYDailySpider(url)
titleGetter = TitleGetter(dmhySpider.get_base_data())

soup1 = dmhySpider.get_html_tree('https://share.dmhy.org'+titleGetter.get_titleList()[0][3][0][0])
list = soup1.find_all('a',{'target','_blank'})
pass


