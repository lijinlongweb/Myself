from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sendMail import sendMail

url=""
#浏览器窗口初始化
browser = webdriver.Chrome()

def login(useDict):#登录
    browser.get(url)
    browser.find_element_by_id("user").send_keys(useDict['user'])
    browser.find_element_by_id("pass").send_keys(useDict['pass'])
    browser.find_element_by_id('loginbtn').click()
    
def loading(First,Second,userDict):#加载框架
    login(userDict)
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='menut%s']/div[2]" %(First)))
        )
        browser.find_element_by_xpath("//div[@id='menut%s']/div[2]" %(First)).click()
    finally:
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='menua%s']/div[%s]" %(First,Second)))
            )
            browser.find_element_by_xpath("//div[@id='menua%s']/div[%s]" %(First,Second)).click()
        finally:
            pass

def search(userDict):#查询成绩
    loading(3,3,userDict)
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
            datas = browser.find_elements_by_xpath("//tbody/tr")
            html = "<html><body><table>"
            for i in range(2, len(datas)):
                html+='<tr>'
                for x in (2, 8, 9):
                    data = browser.find_element_by_xpath("//tbody/tr[%s]/td[%s]" % (i, x)).text
                    html+="<th>%s</th>" %(data)
                html+='</tr>'
            html+= "</table></body></html>"
            sendMail(receiver=userDict["email"],
                     mail_title="期末成绩单",
                     mail_content=html)
                
search(userDict={"user":"","pass":"","email":""})


browser.quit()
