#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time    : 2022/5/19 21:01
# @Author  : Li Hanqing
# @Email   : 1430066373@qq.com

import smtplib
import Common.config as conf
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


def send_mail(addressee):
    mail_host = 'smtp.qq.com'
    username = ''
    password = ''
    receivers = addressee

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header('UI自动化', 'utf-8')
    message['subject'] = Header('UI自动化测试结果', 'utf-8')  # 邮件标题
    message.attach(MIMEText('测试结果详见附件', 'plain', 'utf-8'))  # 邮件正文
    # 构造附件
    report_root = conf.get_value('report_path')  # 获取报告路径
    report_file = 'report.html'  # 报告文件名称
    atta = MIMEText(open(report_root + report_file, 'rb').read(), 'base64', 'utf-8')
    atta["Content-Type"] = 'application/octet-stream'
    atta["Content-Disposition"] = 'attachment; filename={}'.format(report_file)
    message.attach(atta)

    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_host, 25)  # SMTP端口号为25
        smtp.login(username, password)
        smtp.sendmail(username, receivers, message.as_string())
        print('邮件发送成功')
    except Exception as e:
        print('邮件发送失败')
        raise e

