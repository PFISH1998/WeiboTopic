import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

class WeiboMail:

    def __init__(self):
        self._mailHost = 'smtp.qq.com'
        self._user = '1047962209@qq.com'
        self._pass = 'heobyicawgjubcaj'
        self._server = smtplib.SMTP_SSL(self._mailHost, 465)
        self._server.login(self._user, self._pass)

    # content 为发送内容
    def send_mail(self, content='Python邮件发送测试',
                  subject='Python 邮件测试',
                  to_list=['perry1998@outlook.com', '1047962209@qq.com', 'nick250250@qq.com']):
        for to in to_list:
            try:
                message = MIMEText(content, 'plain', 'utf-8')
                message['From'] = formataddr(["WeiboMonitorRobot", self._user])
                message['To'] = formataddr([to, to])
                message['subject'] = subject
                self._server.sendmail(self._user, [to], message.as_string())
                print('发送成功')
            except smtplib.SMTPException:
                print('发送失败')
            finally:
                print('发送完成')
        self._server.close()


m = WeiboMail()
m.send_mail()

