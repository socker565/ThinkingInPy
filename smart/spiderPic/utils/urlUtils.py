# -*-coding:utf-8-*-
import re  # 导入正则表达式模块
import requests  # python HTTP客户端 编写爬虫和测试服务器经常用到的模块

import urllib2
from lxml import etree


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


def getHtml(url, header, timeout):
    htmlData = getHtmlData(url, header, timeout)
    htmlPath = etree.HTML(htmlData)
    return htmlPath


def getHtmlData(url, header, timeout):
    req = urllib2.Request(url, headers=header)
    html = urllib2.urlopen(req, timeout=timeout)
    htmlData = html.read()
    return htmlData
