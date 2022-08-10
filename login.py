# 图形化界面的入口
# (Blame) Ruilin Who
# CoAuthor: Ydy --- ydy2001@buaa.edu.cn

from multiprocessing.sharedctypes import Value
import sys
import json
from main3 import MainUI
from register import RegisterUI

# from nbformat import write
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QLineEdit,  # 输入框
    QPushButton,  # 按钮
    QTextEdit,
    QAction,  # 点击菜单所对应的行为
    QLabel,
    QScrollArea,
    QMessageBox,  # 消息框
    QInputDialog,
)
from PyQt5.QtWidgets import (
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt


class LoginUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setup_UI()
        self.setup_logic()

    def setup_UI(self):
        self.setWindowTitle('AweSomeSchedule Login')
        self.resize(1000, 800)
        self.login_window = QWidget()
        self.login_layout = QVBoxLayout()
        self.login_window.setLayout(self.login_layout)
        self.setCentralWidget(self.login_window)

        #self.test_but = QPushButton('test')
        #self.login_layout.addWidget(self.test_but)

        # account
        self.account_label = QLabel('账户: ')
        self.account_line = QLineEdit()
        self.account_line.setPlaceholderText('请输入账户')
        self.add_h(self.account_label, self.account_line)
        # passwd
        self.passwd_label = QLabel('密码: ')
        self.passwd_line = QLineEdit()
        self.passwd_line.setEchoMode(QLineEdit.Password)
        self.passwd_line.setPlaceholderText('请输入密码')
        self.add_h(self.passwd_label, self.passwd_line)
        # buts
        self.confirm_but = QPushButton('确定')
        self.cancel_but = QPushButton('退出')
        self.register_but = QPushButton('注册')
        self.add_h(self.confirm_but, self.cancel_but, self.register_but)

    def add_h(self, *args):
        temp_layout = QHBoxLayout()
        temp_widget = QWidget()
        temp_widget.setLayout(temp_layout)
        for _ in args:
            temp_layout.addWidget(_)
        self.login_layout.addWidget(temp_widget)

    def setup_logic(self):
        self.cancel_but.clicked.connect(self.exit)
        self.confirm_but.clicked.connect(self.confirm)
        self.register_but.clicked.connect(self.register)

    def exit(self):
        self.close()

    def confirm(self):
        account = self.account_line.text()
        passwd = self.passwd_line.text()
        f = open('accounts', 'r')
        strs = f.readlines()
        i = 0
        check = False
        while i < len(strs):
            if strs[i][0:-1] == account and strs[i+1][0:-1] == passwd:
                check = True
                break
            else:
                i += 2
        if check == False:
            self.show_failure_msg('登陆失败', '账号或密码错误')
            return
        main_ui.show()
        self.close()
        main_ui.current_user = account

    def register(self):
        register_ui.show()

    # $(ruilin) utils: 该函数根据输入的标题和文字显示对应“错误消息框”
    def show_failure_msg(self, title: str, text: str) -> None:
        # msgbox = QMessageBox.information(self, title, text, QMessageBox.Ok)
        msgbox = QMessageBox()
        msgbox.setWindowTitle(title)
        msgbox.setText(text)
        # msgbox.setIcon(QMessageBox.Critical)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setStyleSheet('''QLabel{min-width:300px; min-height:150px}''')
        msgbox.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_ui = LoginUI()
    login_ui.show()
    main_ui = MainUI()
    register_ui = RegisterUI()
    sys.exit(app.exec_())
