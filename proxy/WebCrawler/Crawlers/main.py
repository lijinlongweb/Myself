import requests
from bs4 import BeautifulSoup
from WebCrawler.models import ProxyMessage

def _IP_Test(data):
    if data.Area == "China":
        url = "www.baidu.com"
    else:
        url = "cathaysiansky.blogspot.com"
    if data.Type in ("http", "Http", "HTTP"):
        url = "http://" + url
        testProxies = {"http": "http://{0}:{1}".format(data.IP, data.Port)}
    else:
        url = "https://" + url
        testProxies = {"https": "http://{0}:{1}".format(data.IP, data.Port)}
    try:
        if requests.get(url=url, proxies=testProxies, timeout=3).status_code == 200:
            return True
    except:  # 捕捉
        return False


def _IP_Clear():
    for each in ProxyMessage.objects.all():
        if _IP_Test(each):
            continue
        each.delete()


class GetProxy():
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'Proxy-Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39',
        }
    
    def from_proxy_mimvp_com(self):
        # TODO 该网站端口号使用图片
        pass
    
    def from_www_kuaidaili_com(self):
        # TODO 该网站使用js加载页面
        pass
    
    def from_www_goubanjia_com(self):
        # TODO 该网站使用js重新加载端口 爬到的端口是假的，Fuck you
        pass
    
    def from_www_xicidaili_com(self):
        
        def dealHtml(html):
            for each in html.find_all("tr", class_="odd"):
                try:
                    data = ProxyMessage(
                        IP=each.contents[3].text,
                        Port=each.contents[5].text,
                        Area="China",
                        Address=each.contents[7].find("a").text,
                        Type=each.contents[11].text
                    )
                except:
                    continue
                if _IP_Test(data):
                    data.save()
            for each in html.find_all("tr", class_=""):
                try:
                    data = ProxyMessage(
                        IP=each.contents[3].text,
                        Port=each.contents[5].text,
                        Area="China",
                        Address=each.contents[7].find("a").text,
                        Type=each.contents[11].text
                    )
                except:
                    continue
                if _IP_Test(data):
                    data.save()
        
        for each in range(1, 6):
            url = "http://www.xicidaili.com/nn/{}".format(each)
            dealHtml(BeautifulSoup(requests.get(url, headers=self.headers).text, "lxml").find("table", id="ip_list"))
    
    def GETMORE(self):
        self.from_www_xicidaili_com()
