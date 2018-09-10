import re


def test():
    print(re.match('com', 'www.runoob.com'))  # 不在起始位置匹配
    print(re.match('www', 'www.runoob.com').span())  # 在起始位置匹配

    print(re.search('www', 'www.runoob.com').span())  # 在起始位置匹配
    print(re.search('com', 'www.runoob.com').span())  # 不在起始位置匹配

    line = "Cats are smarter than dogs"

    matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)

    if matchObj:
        print("matchObj.group() : ", matchObj.group())
        print("matchObj.group(1) : ", matchObj.group(1))
        print("matchObj.group(2) : ", matchObj.group(2))
    else:
        print("No match!!")

    print(re.search(r'src=http://www.lofter.com/control\?blogId=(.*)',
                    "src=http://www.lofter.com/control?blogId=4520906", re.M | re.I).group(1))  # 在起始位置匹配


def getUrlName(url):
    return url.split("/")[-1]


def lofter_name():
    imgurl = 'http://imglf6.nosdn0.126.net/img/eHJBeHlSUFlxWXd6REQ0eVJnVEtjZG41ZTNFTzFqSlVORkwzaU5hSkdONzRxcFVmM2RvM1V3PT0.jpg?imageView&thumbnail=1680x0&quality=96&stripmeta=0&type=jpg'
    print(re.search(r'(jpg|png|gif)', imgurl).group(0))
    print(getUrlName(imgurl.split("?")[0]))

lofter_name()
