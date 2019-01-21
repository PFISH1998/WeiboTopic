import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formataddr
from HotTopic import HotTopicChoose
from pyhtml import HTML

# , '330170928@qq.com'
class WeiboMail:

    def __init__(self):
        self._mailHost = 'smtp.qq.com'
        self._user = '1047962209@qq.com'
        self._pass = 'heobyicawgjubcaj'
        self._start_time = time.time()
        self._server = smtplib.SMTP_SSL(self._mailHost, 465)
        self._server.login(self._user, self._pass)

    # content 为发送内容
    def send_mail(self, content='Python邮件发送测试',
                  subject='weiboRobotNote',
                  to_list=['perry1998@outlook.com', '1047962209@qq.com', 'nick250250@qq.com']):
        for to in to_list:
            try:
                message = MIMEText(content, 'html', 'utf-8')
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

    def html_content(self):
        h = HotTopicChoose()
        html = HTML()
        main_html = html.MailHTML
        table_html = html.TABLE_TMPL
        table_list = []
        for line in h.get_day():
            href = "https://s.weibo.com/weibo?q=%s" % line['title']
            line.update({'href': href})
            table_list.append(table_html.format(**line))
        result = ''.join(table_list)
        html_value = dict(
            date_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
            table_tr=result,
            sec=time.time()-self._start_time
        )
        result_html = main_html.format(**html_value)
        return result_html

m = WeiboMail()
content = m.html_content()
m.send_mail(content=content)
