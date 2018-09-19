import urlUtils
import requests
import re
import os
import pkgUtils
import platform


def save_img(html, pattern, path):
    if is_file_exist(path):
        pass
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


def save_images(img_url, path):
    if is_file_exist(path):
        pass
    headers = {
        'User-Agent': urlUtils.getUserAgent(2)}
    for i in range(1, 3):
        try:
            image_request = requests.get(img_url, headers=headers, timeout=20)
            if image_request.status_code == 200:
                open(path, 'wb').write(image_request.content)
                break
        except requests.exceptions.ConnectionError as e:
            print('\tGet %s failed\n\terror:%s' % (img_url, e))
            if i == 1:
                img_url = re.sub('^http://img.*?\.', 'http://img.', img_url)
                print('\tRetry ' + img_url)
            else:
                print('\tRetry fail')
        except Exception as e:
            print(e)
        finally:
            pass


def save_string(str, path):
    if is_file_exist(path):
        pass
    try:
        open(path, 'wb').write(bytes(str.encode("utf-8")))
    except Exception as e:
        print(e)
    finally:
        pass


def _get_path(username):
    path = {
        'Windows': pkgUtils.getLevelPath(-2, '/download/lofter/' + username),
        'Linux': pkgUtils.getLevelPath(-2, '/download/lofter/' + username)
    }.get(platform.system())
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def test_save_string():
    imgurls = {"a", "b", "c"}
    all_img_urls = "\r\n".join(imgurls)
    path = _get_path("vikomo")
    all_img_paths = '%s/%s.%s' % (path, "vikomo", "txt")
    save_string(all_img_urls, all_img_paths)


# print(str(1))
def test(imgPath):
    if os.path.isfile(imgPath):
        print("文件存在")
        pass
    else:
        print("下载中")


def is_file_exist(path):
    return os.path.isfile(path)


if __name__ == '__main__':
    #test(pkgUtils.getLevelPath(-2, '\\download\\lofter\\qyaqy\\2a3d7b945dc4ae7941c2353173ce5e13e.jpg'))
    test_save_string()
