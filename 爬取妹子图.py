from bs4 import BeautifulSoup
import requests
import re
import time
import os
# 初始化数据
RootUrl = r"http://www.mzitu.com"
path = os.getcwd()


def get_image(url, filename):  # 保存图片
    imgPath = os.path.join(path, filename)
    if not os.path.exists(os.path.dirname(imgPath)):  # 探查目录是否存在
        os.makedirs(os.path.dirname(imgPath))  # 建立该目录
    with open(imgPath, "wb") as jpg:  # 保存图片
        try:  # 防止被封
            jpg.write(requests.get(url).content)
        except requests.Timeout:
            time.sleep(1)
            get_image(url, filename)
    print("Save image :"+imgPath)  # 日志
    time.sleep(1)


def get_more_url(Root_Url):  # 获得当前套图
    try:
        imagePage = requests.get(Root_Url)
    except requests.Timeout:
        time.sleep(1)
        get_more_url(Root_Url)
    # 分析页面，获取当前图片链接和下一张图片链接
    text = BeautifulSoup(imagePage.text, "html.parser")
    href = text.find('a', href=re.compile("http://www.mzitu.com/[0-9]+"))
    result = href.find('img').attrs['src']
    # 储存图片
    try:  # 拼接图片文件名称
        name = Root_Url.split('/')
        filename = os.path.join(name[3], name[4]+'.jpg')
    except IndexError:
        filename = os.path.join(name[3], '1.jpg')
    finally:
        get_image(result, filename)
    # 判断是否是最后一张
    if re.match("http://www.mzitu.com/[0-9]+/[0-9]+", href['href']):
        get_more_url(href.attrs['href'])
    else:
        return 1


def get_img_url(MoniUrl):  # 获得当前页面妹子图链接
    page = requests.get(RootUrl)
    text = BeautifulSoup(page.text, "html.parser")
    list = text.find_all(href=re.compile("http://www.mzitu.com/[0-9]+"))
    imgList = [one['href'] for one in list]
    return set(imgList)  # set保证不会有重复链接


for one in get_img_url(RootUrl):
    get_more_url(one)
