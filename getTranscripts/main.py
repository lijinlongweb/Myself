from requests import Session
from bs4 import BeautifulSoup
from sendMail import sendMail


def getTranscripts(userDict, year, semester):
    userdata = Session()
    getJson = userdata.post(
        "http://mjwgl.ahnu.edu.cn/login/remotelogin",
        data={
            "username": userDict["username"],
            "password": userDict["password"],
            "usertype": "stu",
            "device": "aphone",
            "sessionid": ""
        })
    userdata.post(
        getJson.json()["homeurl"],
        data={"requesttype": "cjcx",
              "sessionid": getJson.json()["sessionid"]})
    result = userdata.get(
        "http://mjwgl.ahnu.edu.cn/query/cjquery/index?action=ok&xkxn=%s&xkxq=%s" % (year, semester))
    page = result.content.decode("utf-8")
    text = BeautifulSoup(page, "lxml")
    html = "<html><body><table>"
    for each in text.find_all("tr"):
        count = 0
        html += "<tr>"
        for one in each.children:
            if count in (3, 5, 7, 9):
                if one.text == "" and count == 9:
                    break
                html += str(one)
            count += 1
        else:
            html += "</tr>"
            continue
        break
    else:
        html += "</table></body></html>"
        
        sendMail(
            receiver=userDict["email"], mail_title="期末成绩单", mail_content=html)

