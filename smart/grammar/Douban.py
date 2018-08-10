from urllib.request import urlopen
import threading
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import os


# 主函数
def main():
    driver = webdriver.Firefox()
    driver.get("https://mm.taobao.com/search_tstar_model.htm?")
    bsObj = BeautifulSoup(driver.page_source, "lxml")
    fp = open('mm.txt', 'w+')
    fp.write(driver.find_element_by_id("J_GirlsList").text)
    MMsinfoUrl = bsObj.findAll("a", {"href": re.compile("\/\/.*\.htm\?(userId=)\d*")})
    imagesUrl = bsObj.findAll("img", {"src": re.compile("gtd.*\.jpg")})
    fp.close()
    fp = open('mm.txt', 'r+')
    items = fp.readlines()
    content1 = []
    n = 0
    m = 1
    while (i < 5):
        print("MM's name:" + contents[i][0][0] + "with" + contents[i][0][1])
        print("saving......" + contents[i][0][0] + "in the folder")
        perMMpageUrl = "https:" + contents[i][1]
        path = '/home/lgz/pythontest/mmphoto/' + contents[i][0][0]
        mkdir(path)
        getperMMpageImg(perMMpageUrl, path)
        i += 1
    fp.flush()
    fp.close()

    number = 1
    for imageUrl in imagesUrl:
        url = "https:" + str(imageUrl["src"])
        html = urlopen(url)
        data = html.read()
        fileName = '/home/lgz/pythontest/mmphoto/mm' + str(number) + '.jpeg'
        fph = open(fileName, "wb")
        print("loading MM......" + fileName)
        fph.write(data)
        fph.flush()
        fph.close()
        number += 1

    driver.close()


def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        print("to create a new folder named" + path)
        os.makedirs(path)
    else:
        print("create complete!")


def getperMMpageImg(MMURL, MMpath):
    owndriver = webdriver.Firefox()
    owndriver.get(MMURL)
    ownObj = BeautifulSoup(owndriver.page_source, "lxml")
    perMMimgs = ownObj.findAll("img", {"src": re.compile("\/\/img\.alicdn.*\.jpg")})
    number = 2
    for perMMimg in perMMimgs:
        ImgPath = "https:" + str(perMMimg["src"])
        print(ImgPath)
        try:
            html = urlopen(ImgPath)
            data = html.read()
            fileName = MMpath + "/" + str(number) + '.jpg'
            fp = open(fileName, 'wb')
            print("loading her photo as" + fileName)
            fp.write(data)
            fp.flush()
            fp.close()
            number += 1
        except Exception:
            print("Address Error!!!!!!!!!!!!!!!!!!!!")


if __name__ == '__main__':
    main()