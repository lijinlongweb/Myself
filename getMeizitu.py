from bs4 import BeautifulSoup
import requests
import re
import time
import os
# 初始化数据
RootUrl = r"http://www.mzitu.com/all"
path = os.path.join(os.getcwd(), 'meizitu')

# 定制响应头
Headers = {
    'Accept-Encoding':
    r'gzip, deflate',
    'Accept-Language':
    r'zh-CN,zh;q=0.8',
    'Cache-Control':
    r'max-age=0',
    'DNT':
    r'1',
    'Referer':
    '',
    'Upgrade-Insecure-Requests':
    r'1',
    'Proxy-Connection':
    r'keep-alive',
    'Host':
    r'i.meizitu.net',
    'User-Agent':
    r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39'
}


def get_image(url, filename, headers):  # 保存图片
    imgPath = os.path.join(path, filename)
    if os.path.exists(imgPath) and os.path.getsize(imgPath) > 10000:  # 查重
        return
    else:
        if not os.path.exists(os.path.dirname(imgPath)):  # 探查目录是否存在
            os.makedirs(os.path.dirname(imgPath))  # 建立该目录
        while True:
            try:  # 防止网络超时
                image = requests.get(url, headers=headers, timeout=3).content  # 获取图片二进制
                with open(imgPath, "wb") as jpg:  # 保存图片
                    jpg.write(image)
            except requests.Timeout:
                time.sleep(1)
                continue
            if os.path.getsize(imgPath) > 10000:  # 如果图片获取成功则跳出
                break
            else:
                time.sleep(3)


def get_more_url(Root_Url):  # 递归获得当前套图
    while True:  # 死循环处理网页内容获取
        try:
            imagePage = requests.get(Root_Url, timeout=3)
        except Exception:  # 处理异常
            time.sleep(1)
            continue
        # 分析页面，获取当前图片链接和下一张图片链接
        text = BeautifulSoup(imagePage.text, "html.parser")
        href = text.find('a', href=re.compile("http://www.mzitu.com/[0-9]+"))
        try:  # 此处应是网络问题导致无法找到对应标签
            result = href.find('img').attrs['src']
            break  # 正确解析网页则跳出
        except AttributeError:
            pass
    # 储存图片
    try:  # 拼接图片文件名称
        name = Root_Url.split('/')
        filename = os.path.join(name[3], name[4] + '.jpg')
        if int(name[4]) > 10:
            print("\b\b" + name[4], end='', flush=True)
        else:
            print("\b" + name[4], end='', flush=True)
    except IndexError:
        filename = os.path.join(name[3], '1.jpg')
        print('   1', end='', flush=True)
    finally:
        Headers['Referer'] = Root_Url
        get_image(result, filename, Headers)  # 调用函数保存图片
    # 判断是否是最后一张
    if re.match("http://www.mzitu.com/[0-9]+/[0-9]+", href['href']):
        get_more_url(href.attrs['href'])
    else:  # 递归结束
        print('\n', flush=True)
        return 1


def get_img_url(MoniUrl):  # 获得当前页面妹子图链接
    page = requests.get(MoniUrl)
    text = BeautifulSoup(page.text, "html.parser")
    list = text.find_all(href=re.compile("http://www.mzitu.com/[0-9]+"))
    imgList = [one['href'] for one in list]
    return set(imgList)  # set防止重复的url


if __name__ == '__main__':
    while True:
        for one in get_img_url(RootUrl):
            NOW_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(NOW_TIME + " Save File from:" + one, end='', flush=True)
            get_more_url(one)

