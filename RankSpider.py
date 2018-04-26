# python原生请求
import re
from urllib import request

import time

is_exit = True


# 三种匹配字符的方式
# /w 单词字符 /W
# /s 空白字符 /S
# . 匹配除了/n的全部字符

class BaseSpider(object):
    """
    爬虫基类
    """

    base_url = 'https://www.panda.tv'

    def __init__(self):
        pass

    def count_time(func):
        """
        统计执行时间
        """

        def wrapper(*args, **keyword):
            t1 = time.time()
            print(0)
            func(*args, **keyword)
            t2 = time.time()
            print(t2 - t1)

        return wrapper

    def fetch_content(self, url):
        """
        读取网页
        """

        r = request.urlopen(BaseSpider.base_url + url)
        htmls = r.read()
        htmls = str(htmls, encoding='UTF-8')
        return htmls

    def sorted(self, anchors, sort_seed, reverse=True):
        """
        对数据排序
        """

        anchors = sorted(anchors, key=sort_seed, reverse=reverse)
        return anchors


class CateSpider(BaseSpider):
    cate_url = '/cate'
    root_pattern = '<a class="video-list-item-wrap" ([\s\S]*?)</a>'
    url_pattern = 'href="([\s\S]*?)"'
    name_pattern = '<div class="cate-title">([\s\S]*?)</div>'

    def __init__(self):
        super(CateSpider, self).__init__()

    def __analysis(self, htmls):
        """
        解析网页数据，爬取需求信息

        :param htmls: 需要解析的网页
        :return: 解析得到的字典数据
        """

        # 选取唯一性的标签
        root_html = re.findall(CateSpider.root_pattern, htmls)
        anchors = []
        for html in root_html:
            url = re.findall(CateSpider.url_pattern, html)
            name = re.findall(CateSpider.name_pattern, html)
            anchor = {'url': url, 'name': name}
            anchors.append(anchor)
        return anchors

    def __refine(self, anchors):
        """
        美化数据，剔除多余信息
        """

        # strip去除换行与空格
        l = lambda anchor: {'name': anchor['name'][0].strip(), 'url': anchor['url'][0]}
        return list(map(l, anchors))

    def __filter_seed_cate(self, anchors):
        """
        排序核心依据
        """
        if '/cate' in anchors['url']:
            return True
        return False

    def __show(self, anchors):
        for index in range(0, len(anchors)):
            print(str(index + 1) + ".", ' 频道：' + anchors[index]['name'], ' url：' + str(anchors[index]['url']))

    def go(self):
        htmls = self.fetch_content(CateSpider.cate_url)
        anchors = self.__analysis(htmls)
        anchors = self.__refine(anchors)
        anchors = list(filter(self.__filter_seed_cate, anchors))
        self.__show(anchors)
        return anchors


class RankSpider(BaseSpider):
    # ? 表示非贪婪模式
    # 贪婪模式（默认）：找到了第一个就不找了
    # 非贪婪模式：找到所有匹配
    # 匹配所有字符串：([\s\S]*?)
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '<span class="video-nickname" title="([\s\S]*?)">'
    number_pattern = '<i class="video-station-num">([\s\S]*?)人</i>'
    hot_number_pattern = '<span class="video-number">([\s\S]*?)</span>'

    def __init__(self, url):
        super(RankSpider, self).__init__()
        self.url = url

    def __analysis(self, htmls):
        """
        解析网页数据，爬取需求信息

        :param htmls: 需要解析的网页
        :return: 解析得到的字典数据
        """

        # 选取唯一性的标签
        root_html = re.findall(RankSpider.root_pattern, htmls)
        anchors = []
        for html in root_html:
            name = re.findall(RankSpider.name_pattern, html)
            number = re.findall(RankSpider.number_pattern, html)
            hot = re.findall(RankSpider.hot_number_pattern, html)
            anchor = {'name': name, 'number': number, 'hot': hot}
            anchors.append(anchor)
        return anchors

    def __refine(self, anchors):
        """
        美化数据，剔除多余信息
        """

        # strip去除换行与空格
        l = lambda anchor: {'name': anchor['name'][0].strip(),
                            'number': int(anchor['number'][0]),
                            'hot': anchor['hot'][0]}
        return list(map(l, anchors))

    def __sort_seed_hot(self, anchor):
        """
        根据人气排序
        """

        r = re.findall("\d*", anchor['hot'])
        number = float(r[0])
        if '万' in anchor['hot']:
            number *= 10000
        return number

    def __sort_seed_number(self, anchor):
        """
        根据车票排序
        """

        return anchor['number']

    def __show(self, anchors):
        for index in range(0, len(anchors)):
            print(str(index + 1) + ".", '主播名字：' + anchors[index]['name'], '  人气：' + str(anchors[index]['hot']),
                  '  车票：' + str(anchors[index]['number']))

    @BaseSpider.count_time
    def go(self):
        htmls = self.fetch_content(self.url)
        anchors = self.__analysis(htmls)
        result = self.__refine(anchors)
        anchors = self.sorted(result, self.__sort_seed_number)
        self.__show(anchors)


while is_exit:
    c = CateSpider()
    rate_anchors = c.go()
    cate_number = input("请输入想要查看的频道号码：")
    if 'exit' == cate_number:
        break
    s = RankSpider(rate_anchors[int(cate_number) - 1]['url'])
    s.go()
