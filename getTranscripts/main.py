from requests import Session
from bs4 import BeautifulSoup
from sendMail import sendMail


def getTranscripts(userDict):
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
    result = userdata.post(
        getJson.json()["homeurl"],
        data={"requesttype": "cjcx",
              "sessionid": getJson.json()["sessionid"]})
    page = result.content.decode("utf-8")
    text = BeautifulSoup(page, "lxml")
    html = "<html><body><table>"
    for each in text.find_all("tr"):
        count = 0
        html += "<tr>"
        for one in each.children:
            if count in (3, 5, 7, 9):
                if one.text == "":
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


userDict = {
    "username": "16111204040",
    "password": "123456789",
    "email": "1191170766@qq.com"
}
getTranscripts(userDict)
