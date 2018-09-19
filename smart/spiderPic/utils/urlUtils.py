# -*-coding:utf-8-*-
import re  # 导入正则表达式模块
import requests  # python HTTP客户端 编写爬虫和测试服务器经常用到的模块

from lxml import etree
from urllib.request import urlopen
from urllib.request import Request


def getHtml(url, header, timeout):
    htmlData = getHtmlData(url, header, timeout)
    htmlPath = etree.HTML(htmlData)
    return htmlPath


def getHtmlData(url, header, timeout):
    req = Request(url, headers=header)
    html = urlopen(req, timeout=timeout)
    htmlData = html.read()  # str(html.read(), 'utf-8')
    return htmlData


def getUserAgent(type):
    if type == 1:
        return "Mozilla/6.0 (Windows NT 7.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.15.2743.116 Safari/57.36"
    elif type == 2:
        return 'Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.11.3325.146 Safari/27.36'
    elif type == 3:
        return 'Mozilla/7.0 (Windows NT 9.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.20.33.146 Safari/17.36'
    elif type == 4:
        return 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'
    elif type == 5:
        return 'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0'
    elif type == 6:
        return 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19'
    elif type == 7:
        return 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    return "Mozilla/8.0 (Windows NT 10.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.21.27.116 Safari/47.36"


def saveDoc(html, pattern, path):
    for addr in re.findall(pattern, html, re.S):  # 查找URL
        print('正在爬取URL地址：' + str(addr))  # [0:30] + '...')  # 爬取的地址长度超过30时，用'...'代替后面的内容
        try:
            pics = requests.get(addr, timeout=10)  # 请求URL时间（最大100秒）
        except requests.exceptions.ConnectionError:
            print('您当前请求的URL地址出现错误')
            continue
        # try:
        file = path + getUrlName(addr)
        fq = open(file, 'wb')  # 下载图片，并保存和命名
        fq.write(pics.content)
        fq.close()


def getUrlName(url):
    return url.split("/")[-1]

# session = requests.session()
# url = 'http://qyaqy.lofter.com'
# # headers在这里不必须，嗯，还是加上吧...
# headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
#     'host': 'zqyjbg.com',
#     'Accept-Language': 'zh-CN,zh;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, sdch',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Upgrade-Insecure-Requests': '1',
#     'Connection': 'keep-alive',
#     'Cookie': ''
# }
# r = session.get(url, headers=headers, verify=False)
# print(r.content)
