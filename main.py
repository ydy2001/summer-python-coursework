# 图形化界面的入口
# (Blame) Ruilin Who

import sys
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QMainWindow,
    QLineEdit,      # 输入框 
    QPushButton,    # 按钮
    QTextEdit,
    QAction,        # 点击菜单所对应的行为
)

from PyQt5.QtCore import Qt
from sqlalchemy import false


class MainUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setup_UI()
    
    def setup_UI(self):
        self.setWindowTitle('AweSomeSchedule')
        self.resize(1200, 1500)

        self.input_box = QLineEdit(self)                # 任务输入框
        self.input_box.setGeometry(400, 100, 600, 100) 


        self.input_but = QPushButton('Input', self)     # 确认输入按钮
        self.input_but.setGeometry(1050, 100, 100, 100)
        self.input_but.clicked.connect(self.input_button_clicked)

        self.init_textbox()
        

        action0 = QAction("月历模式", self)
        action1 = QAction("重要性模式", self)
        # menubar = self.menuBar()

        toolbar = self.addToolBar('this is toolbar')
        toolbar.setMovable(False)
        toolbar.setFixedWidth(200)
        toolbar.setOrientation(Qt.Vertical)

        toolbar.addAction(action0)
        toolbar.addAction(action1)


    def input_button_clicked(self):
        self.msg_box.append(self.input_box.text())

    def init_textbox(self):
        self.msg_box = QTextEdit(self)                   # 任务主显示框
        self.msg_box.setGeometry(400, 300, 750, 1000)
        self.msg_box.append('+---标题----+-----截止日期----+---重要性---+-')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_ui = MainUI()
    main_ui.show()
    sys.exit(app.exec_())
