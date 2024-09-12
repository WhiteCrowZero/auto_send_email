import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QMessageBox, QGroupBox
)
from auto_send_email import AutoSendEmail


class EmailSenderApp(QWidget):
    def __init__(self):
        super().__init__()

        # 初始参数设置
        self.smtp_server = 'smtp.163.com'
        self.smtp_port = '465'
        self.smtp_username = 'example@163.com'
        self.smtp_password = 'password'
        self.receivers = 'example@qq.com example@qq.com example@qq.com example@qq.com'
        self.subject = 'TEST'
        self.template_file = 'email_template.html'
        self.images_json = 'image_mapping.json'

        self.initUI()

    def initUI(self):
        # 创建界面元素
        server_label = QLabel('SMTP Server:')
        self.server_edit = QLineEdit(self.smtp_server)
        self.server_edit.setPlaceholderText('Enter SMTP Server')

        port_label = QLabel('SMTP Port:')
        self.port_edit = QLineEdit(self.smtp_port)
        self.port_edit.setPlaceholderText('Enter SMTP Port')

        username_label = QLabel('SMTP Username:')
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText('Enter SMTP Username')

        password_label = QLabel('SMTP Password:')
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText('Enter SMTP Password')

        receivers_label = QLabel('Receivers (comma-separated):')
        self.receivers_edit = QLineEdit()
        self.receivers_edit.setPlaceholderText('Enter Receiver Emails')

        subject_label = QLabel('Email Subject:')
        self.subject_edit = QLineEdit()
        self.subject_edit.setPlaceholderText('Enter Email Subject')

        template_label = QLabel('Email Template File:')
        self.template_edit = QLineEdit(self.template_file)
        self.template_edit.setPlaceholderText('Select Email Template File')

        images_label = QLabel('Images JSON File:')
        self.images_edit = QLineEdit(self.images_json)
        self.images_edit.setPlaceholderText('Select Images JSON File')

        # 加载样式表
        with open('styles.qss', 'r') as styles:
            self.setStyleSheet(styles.read())

        # 设置密码框为密码输入模式
        # self.password_edit.setEchoMode(QLineEdit.Password)

        # 创建浏览按钮
        template_button = QPushButton('Browse...')
        template_button.clicked.connect(self.browse_template)
        images_button = QPushButton('Browse...')
        images_button.clicked.connect(self.browse_images)

        # 创建发送按钮
        send_button = QPushButton('Send Email')
        send_button.clicked.connect(self.send_email)

        # 创建布局
        main_layout = QVBoxLayout()

        # SMTP设置区域
        smtp_groupbox = QGroupBox('SMTP Settings')
        smtp_layout = QVBoxLayout()
        smtp_layout.addWidget(server_label)
        smtp_layout.addWidget(self.server_edit)
        smtp_layout.addWidget(port_label)
        smtp_layout.addWidget(self.port_edit)
        smtp_layout.addWidget(username_label)
        smtp_layout.addWidget(self.username_edit)
        smtp_layout.addWidget(password_label)
        smtp_layout.addWidget(self.password_edit)
        smtp_groupbox.setLayout(smtp_layout)
        main_layout.addWidget(smtp_groupbox)

        # 收件人和主题区域
        receivers_groupbox = QGroupBox('Email Details')
        receivers_layout = QVBoxLayout()
        receivers_layout.addWidget(receivers_label)
        receivers_layout.addWidget(self.receivers_edit)
        receivers_layout.addWidget(subject_label)
        receivers_layout.addWidget(self.subject_edit)
        receivers_groupbox.setLayout(receivers_layout)
        main_layout.addWidget(receivers_groupbox)

        # 文件选择区域
        file_groupbox = QGroupBox('File Selection')
        file_layout = QVBoxLayout()
        file_layout.addWidget(template_label)
        hbox_template = QHBoxLayout()
        hbox_template.addWidget(self.template_edit)
        hbox_template.addWidget(template_button)
        file_layout.addLayout(hbox_template)
        file_layout.addWidget(images_label)
        hbox_images = QHBoxLayout()
        hbox_images.addWidget(self.images_edit)
        hbox_images.addWidget(images_button)
        file_layout.addLayout(hbox_images)
        file_groupbox.setLayout(file_layout)
        main_layout.addWidget(file_groupbox)

        # 发送按钮
        main_layout.addWidget(send_button)

        self.setLayout(main_layout)

        # 设置窗口属性
        self.setWindowTitle('Email Sender')
        self.setGeometry(100, 100, 600, 400)
        self.show()

    def browse_template(self):
        # 打开文件对话框选择模板文件
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Email Template File", "", "HTML Files (*.html)", options=options)
        if file_name:
            self.template_edit.setText(file_name)

    def browse_images(self):
        # 打开文件对话框选择图片映射文件
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Images JSON File", "", "JSON Files (*.json)", options=options)
        if file_name:
            self.images_edit.setText(file_name)

    def send_email(self):
        # 获取界面上的参数值
        self.smtp_server = self.server_edit.text()
        self.smtp_port = int(self.port_edit.text())
        self.smtp_username = self.username_edit.text()
        self.smtp_password = self.password_edit.text()
        receivers_text = self.receivers_edit.text().strip()
        self.receivers = [receiver.strip() for receiver in receivers_text.split(' ') if receiver.strip()]
        self.subject = self.subject_edit.text()
        self.template_file = self.template_edit.text()
        self.images_json = self.images_edit.text()

        # 将参数保存到JSON文件中（可选）
        params = {
            'smtp_server': self.smtp_server,
            'smtp_port': self.smtp_port,
            'smtp_username': self.smtp_username,
            'smtp_password': self.smtp_password,
            'receivers': self.receivers,
            'subject': self.subject,
            'template_file': self.template_file,
            'images_json': self.images_json
        }
        with open('email_params.json', 'w') as f:
            json.dump(params, f, indent=4)

        # print(params)
        # 创建邮件发送对象并发送邮件
        auto_sender = AutoSendEmail(self.smtp_server, self.smtp_port, self.smtp_username, self.smtp_password, self.receivers)
        auto_sender.auto_send(self.subject, self.template_file, self.images_json)

        # 显示完成消息框
        QMessageBox.information(self, 'Email Sent', 'Emails have been sent successfully.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EmailSenderApp()
    sys.exit(app.exec_())
