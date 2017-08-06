from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

def sendMail(receiver,mail_title,mail_content):
    #qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    #sender_qq为发件人的qq号码
    sender_qq = '1191170766'
    #pwd为qq邮箱的授权码
    pwd = 'zjqfuioxtozqgjia'
    #发件人的邮箱
    sender_qq_mail = 'chen_ye_119@qq.com'
    #收件人邮箱 receiver
    #邮件的正文内容 mail_content
    #邮件标题 mail_title
    
    #ssl登录
    smtp = SMTP_SSL(host_server)
    #set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(0)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)
    
    msg = MIMEText(mail_content, "html", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = receiver
    
    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()
    
#sendMail(receiver="1191170766@qq.com",mail_title="test",mail_content="这是一个测试")