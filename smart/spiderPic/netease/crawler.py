# !/usr/bin/env python3
#coding=gbk

import requests
from lxml import etree
import re
import os
import multiprocessing
import asyncio
from concurrent import futures
import argparse
import configparser
import shlex
import time


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Upgrade-Insecure-Requests": "1"
    }
PROCESSES = multiprocessing.cpu_count()


def find_latest_page(blogname):
    """ 查找首页, 并返回博客最近更新子页面 """
    url = "http://{}.lofter.com".format(blogname)
    print("尝试下载首页并抓取需要的数据： ", url)
    resp = requests.get(url, headers=HEADERS)
    pattern = re.compile(url+r'(/post/\S+)"')
    url_sub = url + re.search(pattern, resp.text).group(1)
    return url_sub


def page_download_n_parse(url, proxies=None, timeout=None, retry_times=0):
    """博客页面的下载和数据抓取， text 和 tags 按需需要修改"""
    print("尝试下载子页并抓取需要的数据： ", url)
    resp = requests.get(url, headers=HEADERS, proxies=proxies, timeout=timeout)
    if resp.status_code != 200:
        if retry_times < 3:
            print('尝试下载子页途中出现错误，重试' % resp.status_code)
            retry_times +=1
            return page_download_n_parse(url, proxies, timeout, retry_times)
        else:
            print('无法下载页面，请稍后再重试，或使用代理IP。')
    pattern = re.compile(r'<img src="(http://imglf\d?\.(?:nosdn\.127|ph\.126)'
                         r'\.net(?:/img)?/\S+?\.jpg)\S*?"')
    image_urls = re.findall(pattern, resp.text)
    html = etree.HTML(resp.text)
    # 这里只是某个模板的 text 和 tags 抓取方式， 无法通过 re 进行爬取, 只能特定修改。
    text = html.xpath('string(//div[@class="ctc box"]/div[@class="text"])')
    tags = html.xpath('//div[@class="tags box"]/a/text()')

    item = dict()
    item['url'] = url
    item["image_urls"] = image_urls
    if text:
        item["text"] = re.sub(r'\s+',' ',text.strip())
    item["tags"] = tags
    item['proxies'] = proxies

    next_url = html.xpath('//a[@id="__next_permalink__"]/@href')
    if next_url:
        next_url = next_url[0]
    return item, next_url


class ImagesDownloader(object):

    def __init__(self):
        self.redownload_list = []  # 最后再尝试重新下载

    def image_download(self, urls, filename, blogname, proxies=None, timeout=None):
        event_loop = asyncio.new_event_loop()
        event_loop.run_until_complete(self.async_download(urls, filename, blogname,
                                                          proxies, timeout))
        event_loop.close()
        return

    async def async_download(self, urls, filename_raw, blogname, proxies, timeout):
        """ 指定下载路径， 并下载图片。 """
        if not os.path.isdir(blogname):
            os.mkdir(blogname)
        num = 1
        for url in urls:
            if filename_raw is None:
                filename = url.split('/')[-1]
            else:
                if num == 1:
                    filename = filename_raw + '.jpg'
                else:
                    filename = "{0}({1}).jpg".format(filename_raw, str(num))
                num += 1
            file_path = os.path.join(blogname, filename)
            if not os.path.isfile(file_path):
                await self._async_download(url, file_path, proxies, timeout)

    async def _async_download(self, url, file_path, proxies, timeout, retry_times=0):
        """ 下载图片， 出现错误，最多重试三次， . """
        try:
            resp = requests.get(url, proxies=proxies, stream=True,
                                timeout=timeout, headers=HEADERS)
            if resp.status_code != 200:
                raise Exception('尝试下载图片时，出现错误，重试' % resp.status_code)
            with open(file_path, 'wb') as f:
                for chunk in resp.iter_content(1024 * 100):
                    f.write(chunk)
        except Exception as e:
            print("%s: %s" % (e, url))
            # try again
            if retry_times < 3:
                retry_times += 1
                time.sleep(TIMESLEEP)
                # 如需设置proxies, 在下行代码设置设置
                await self._async_download(url, file_path, proxies, timeout, retry_times)
            else:
                print("Download Fail(retried 3 times)： ", url)
                self.redownload_list.append((url, file_path))
        return


class TextWriter(object):
    """把必要的内容文本写入保存"""

    def __init__(self, filename):
        if not os.path.isdir(filename):
            os.mkdir(filename)
        file_path = os.path.join(filename, '0.'+filename+'.txt')
        self.file = open(file_path, 'w')

    def close(self):
        self.file.close()

    def process_item(self, item):
        self.file.write(item['url']+ '\n')
        if item.get("image_urls"):
            for url in item['image_urls']:
                line = url.split('?')[0] + '\n'
                self.file.write(line)

        if item.get('tags'):
            self.file.write('Tags:')
            for tag in item['tags']:
                self.file.write(str(tag.encode('GBK', 'ignore')))
            self.file.write('\n')

        if item.get('text'):
            text = re.sub(r'\xa0|\n', ' ', item['text'].strip())
            text = re.sub(r'\s+', ' ', text).encode('GBK', 'ignore');
            self.file.write(str(text))
        self.file.write('\n\n')

        return


def get_proxies(proxies_list):
    """可以把获取 proxies 函数和 112行，167行代码关联， 设置代理"""
    proxies = proxies_list.pop(0)
    proxies_list.append(proxies)
    return proxies


def main(blogname, timesleep=0):
    """ 多线程处理下载图片部分"""
    url_sub = find_latest_page(blogname)
    image = ImagesDownloader()
    text = TextWriter(blogname)
    with futures.ThreadPoolExecutor(max_workers=PROCESSES*2) as ex:
        while url_sub:
            # 如需设置proxies, 在下行代码设置设置
            item, url_sub = page_download_n_parse(url_sub, proxies=None,
                                                  timeout=TIMEOUT)
            image_urls = item.get('image_urls')
            if image_urls:
                print('尝试下载图片 %s' % image_urls)
                filename = item.get('text')
                if filename:
                    filename = filename if len(filename) < 10 else filename[:10]
                text.process_item(item)
                ex.submit(image.image_download, image_urls, filename, blogname,
                          proxies=item['proxies'], timeout=TIMEOUT)
        time.sleep(timesleep)
    text.close()


# main 部分， 设置 config 和 命令行参数
if __name__ == "__main__":
    config_parser = configparser.ConfigParser()
    config_parser.read('config.ini')
    BLOGNAME = config_parser.get('USER', 'BLOGNAME')
    blognames = shlex.split(BLOGNAME)
    TIMEOUT = config_parser.getint('USER', 'TIMEOUT')
    TIMESLEEP = config_parser.getint('USER', 'TIMESLEEP')

    arg_parser = argparse.ArgumentParser(description="This is a "
                                                     "lofter crawler program.")
    arg_parser.add_argument('-b', '--blogname', action="append",
                            help="Specifies the name(s) of the blog to be crawled")
    args = arg_parser.parse_args()
    if args.blogname:
        blognames = args.blogname
    if blognames:
        for blogname in blognames:
            print('尝试下载博客内容，请稍后： %s' % blogname)
            main(blogname, TIMESLEEP)
            print('下载完毕： %s' % blogname)
    else:
        print('请输入正确的博客英文名。')
