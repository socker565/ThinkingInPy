import urllib2
from lxml import etree


def getHtml(url, header, timeout):
    htmlData = getHtmlData(url, header, timeout)
    htmlPath = etree.HTML(htmlData)
    return htmlPath


def getHtmlData(url, header, timeout):
    req = urllib2.Request(url, headers=header)
    html = urllib2.urlopen(req, timeout=timeout)
    htmlData = html.read()
    return htmlData
