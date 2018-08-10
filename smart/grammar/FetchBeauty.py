# coding = utf-8
import urllib3
import re


# py抓取页面图片并保存到本地

# 获取页面信息
def getHtml(url):
    http = urllib3.PoolManager()
    request = http.request('GET', url)
    html = str(request.data, encoding="utf-8")
    return html


# 通过正则获取图片
def getImg(html):
    reg = r'src="(.+?\.jpg)" pic_ext'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    # 循环把图片存到本地
    return imglist


html = getHtml("http://tieba.baidu.com/p/2460150866")
# print(html)
imglist=getImg(html)
print(imglist)
x = 0
for imgurl in imglist:
    # 保存到本地
    urllib3.urlretrieve(imgurl, '/Applications/MAMP/image/%s.jpg' % x)
    x += 1
