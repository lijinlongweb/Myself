from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
useDict={"user":"16111204040","pass":"123456789","usertype":"stu"}
url="http://jwgl.ahnu.edu.cn/"

#浏览器窗口初始化
browser = webdriver.Chrome()
browser.get(url)
def login():#登录
    browser.find_element_by_id("user").send_keys(useDict['user'])
    browser.find_element_by_id("pass").send_keys(useDict['pass'])
    browser.find_element_by_id('loginbtn').click()
    
def loading():#加载框架
    login()
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='menut3']/div[2]"))
        )
        browser.find_element_by_xpath("//div[@id='menut3']/div[2]").click()
    finally:
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='menua3']/div[3]"))
            )
            browser.find_element_by_xpath("//div[@id='menua3']/div[3]").click()
        finally:
            pass

def search():#查询成绩
    loading()
    browser.switch_to_frame('mainframe')
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "xkxn"))
        )
        browser.find_element_by_xpath("//select[@id='xkxn']/option[3]").click()
    finally:
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "xkxq"))
            )
            browser.find_element_by_xpath("//select[@id='xkxq']/option[3]").click()
        finally:
            datas=browser.find_elements_by_xpath("//tbody/tr")
            for i in range(2, len(datas)):
                for x in (2,8,9):
                    data=browser.find_element_by_xpath("//tbody/tr[%s]/td[%s]" %(i,x)).text
                    print(data,end=' ')
                print("")
                
    browser.close()

search()

browser.quit()
