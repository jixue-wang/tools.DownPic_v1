""" 以实现多线程"""

import requests
from bs4 import BeautifulSoup
import time
import random
import re
import os
import sys
from concurrent.futures import ThreadPoolExecutor
import glob


headers = {

}


# 1.获取url响应
def response(url):
    resp = requests.get(url=url, headers=headers)
    time.sleep(random.randint(2, 3))
    resp.encoding = resp.apparent_encoding  # print("正在传送response")
    return resp


# 2.实例化BeautifulSoup 解析出图片的详情页url地址
def Sour_all(hp_list):
    all_list = []
    if len(hp_list) != 0:
        for html_url in hp_list:
            time.sleep(random.randint(1, 4))

            resp = response(html_url)
            soup = BeautifulSoup(resp.text, "lxml")  # 容易忘记填写"lxml"或者"html.parse"
            if soup.find_all("a", attrs={"class": "item-link"}):
                page_list = re.findall(r'https://f2mm\.com.*\.html', str(soup))
                # print(page_list)
                for href_page in page_list:
                    a_resp = response(href_page)
                    a_soup = BeautifulSoup(a_resp.text, "lxml")
                    # print(a_soup)

                    img_cont = str(a_soup)
                    pagelist = re.findall(r'data-src=\"(https.*\.jpg)\"', img_cont)
                    kick_more = (list(set(pagelist)))
                    for i in kick_more:
                        all_list.append(i)
                        print('\r已加载完{}条图片数据'.format(len(all_list)), end='')
    return all_list

def get_filecont(file_name):
    dp_list = []

    rfile = open(file_name, 'r', encoding='utf-8')
    lines = rfile.readlines()
    print('~~~~~读取列表中,共计'+str(sum([1 for i in open(file_name,"r").readlines() if i.strip()]))+'条~~~~~')
    sum_ser,sum_lst = 0,0
    for n,line in enumerate(lines):
        if line not in ['\r\n','\n']:
            time.sleep(random.randint(2, 3))
            resp = response(line.strip())
            soup = BeautifulSoup(resp.text, "lxml")  # 容易忘记填写"lxml"或者"html.parse"

            if not soup.find_all("a", attrs={"class": "item-link"}):

                num = re.findall('该图集包含(\d+)张照片，更新于', str(soup))
                sum_lst += int(num[0])
                page_list = (re.findall(r'data-src=\"(https.*\.jpg)\"', str(soup)))

                for i in page_list:
                    dp_list.append(i)
                print('\r已加载完{}条图片数据'.format((sum_lst)), end='')
    return dp_list


def download(i,out_dir = '.\\01'):

    imgname = i.split('/')[-2] + '_' + i.split('/')[-1]
    time.sleep(random.randint(2, 3))
    # #开始下载
    res = requests.get(i)

    if not os.path.exists(out_dir + os.sep + imgname):

        with open(out_dir + os.sep + imgname, 'wb') as f: 
            f.write(res.content)
            # time.sleep(3)


if __name__ == '__main__':  # 一张一张的下载太慢了  简单开个进程池 图片太多开双进程池

    file_name = sys.argv[1]
    dp_list = get_filecont(file_name)

    ''' 列表'''
    if len(dp_list) != 0:
        # Soup_list(dp_list)
        print("\n~~~~开始下载~~~~", end='')
        with ThreadPoolExecutor(max_workers=100) as t:
            for i in dp_list:
                t.submit(download, i)
        print("\r~~~~下载完成啦~~~~", end='')

