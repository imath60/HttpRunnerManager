import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os

from HttpRunnerManager.settings import EMAIL_SEND_USERNAME, EMAIL_SEND_PASSWORD

from dingtalkchatbot.chatbot import DingtalkChatbot


def send_dingtalk_alert(report_url, name, testsRun, success, unsuccess):
    title = "定时任务【%s】测试报告" % name
    text = "执行用例数【%s】\n成功用例数【%s】\n失败用例数【%s】" % (testsRun, success, unsuccess)
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=b2b8573a3f5e8685fa504f1fa6fe084c7b33303ed5291d0bcae6a594b12a6914'
    xiaoding = DingtalkChatbot(webhook)
    xiaoding.send_link(title=title, text=text, message_url=report_url)


def send_email_reports(receiver, html_report_path):
    if '@sina.com' in EMAIL_SEND_USERNAME:
        smtp_server = 'smtp.sina.com'
    elif '@163.com' in EMAIL_SEND_USERNAME:
        smtp_server = 'smtp.163.com'
    else:
        smtp_server = 'smtp.exmail.qq.com'

    subject = "接口自动化测试报告"

    with io.open(html_report_path, 'r', encoding='utf-8') as stream:
        send_file = stream.read()

    att = MIMEText(send_file, "base64", "utf-8")
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = "attachment;filename = TestReports.html"

    body = MIMEText("附件为定时任务生成的接口测试报告，请查收，谢谢！", _subtype='html', _charset='gb2312')

    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['from'] = EMAIL_SEND_USERNAME
    msg['to'] = receiver
    msg.attach(att)
    msg.attach(body)

    smtp = smtplib.SMTP()
    smtp.connect(smtp_server)
    smtp.starttls()
    smtp.login(EMAIL_SEND_USERNAME, EMAIL_SEND_PASSWORD)
    smtp.sendmail(EMAIL_SEND_USERNAME, receiver.split(','), msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    send_email_reports('liuyuan2680@ipalfish.com', '/Users/yuxin/Downloads/1555658400.html')
