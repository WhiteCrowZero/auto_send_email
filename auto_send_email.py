import base64
import json
import logging
import re
import socket
import threading
import time
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
# 配置邮件服务器和账户信息
# 网易
smtp_server = 'smtp.163.com'
smtp_port = 465
smtp_username = 'zerowhite2048@163.com'
smtp_password = 'OUQEXYNLEBYLYUNG'
sender = 'zerowhite2048@163.com'


# QQ
smtp_server = 'smtp.qq.com'
smtp_port = 587
smtp_username = '3275036853@qq.com'
smtp_password = 'vngatnovzcfzcjcf'
sender = '3275036853@qq.com'
"""

class AutoSendEmail:
    def __init__(self, smtp_server, smtp_port, smtp_username, smtp_password, receivers):
        # 配置邮件服务器和账户信息
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.sender = smtp_username
        # 收件人列表
        self.receivers = receivers

    # 读取HTML邮件模板文件，并将图像嵌入其中
    def read_html_template_with_images(self, template_file, images_json):
        with open(template_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 打开并读取JSON文件
        with open(images_json, 'r', encoding='utf-8') as json_file:
            images = json.load(json_file)

        # 替换HTML中的图像占位符为base64编码的图像
        for placeholder, image_path in images.items():
            with open(image_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
            img_tag = f'data:image/png;base64,{img_data}'
            html_content = re.sub(f'{{{{ {placeholder} }}}}', img_tag, html_content)

        return html_content

    # 准备发送邮件的内容
    def send_email(self, receiver, subject, html_content):
        try:
            # 创建一个MIMEMultipart对象
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = self.sender
            msg['To'] = receiver

            # 将HTML内容转换为MIMEText对象
            msg.attach(MIMEText(html_content, 'html'))

            # 记录邮件发送信息到日志
            log_message = f"Send Time：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, sender：{self.sender}, receiver：{receiver}"
            logging.info(log_message)

            # 记录当前工作电脑的IP地址到日志
            current_ip = socket.gethostbyname(socket.gethostname())
            logging.info(f"IP address: {current_ip}")

            # 连接到邮件服务器并发送邮件
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as smtp:
                smtp.login(self.smtp_username, self.smtp_password)
                smtp.sendmail(self.sender, receiver, msg.as_string())
                print(f"Email successfully sent to {receiver}.")
        except Exception as e:
            print(f"Error sending email to {receiver}: {str(e)}")
            logging.error(f"Failed to send email to {receiver}: {str(e)}")

    def auto_send(self, subject, template_file, images_json):
        # 设置日志配置
        logging.basicConfig(filename='email_logs.log', level=logging.INFO,
                            format='%(asctime)s - %(message)s', encoding='utf-8')

        # 记录开始时间
        start_time = time.time()

        # 读取HTML邮件模板内容
        html_content = self.read_html_template_with_images(template_file, images_json)

        # 多线程发送邮件
        threads = []
        for receiver in self.receivers:
            thread = threading.Thread(target=self.send_email, args=(receiver, subject, html_content))
            threads.append(thread)
            thread.start()

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        # 记录结束时间和总耗时
        end_time = time.time()
        total_time = end_time - start_time
        logging.info(f"Total elapsed time for sending emails: {total_time} seconds")
        logging.info("----------------------------------------")

        print("All emails have been sent.")


# Example usage
if __name__ == '__main__':
    smtp_server = 'smtp.163.com'
    smtp_port = 465
    smtp_username = 'zerowhite2048@163.com'
    smtp_password = 'OUQEXYNLEBYLYUNG'
    # receivers = ['3633850267@qq.com', 'xxy050905@qq.com','309701741@qq.com']
    receivers = ['3633850267@qq.com']

    subject = 'Test Email Subject'
    template_file = 'email_template.html'
    images_json = 'image_mapping.json'

    auto_sender = AutoSendEmail(smtp_server, smtp_port, smtp_username, smtp_password, receivers)
    auto_sender.auto_send(subject, template_file, images_json)
