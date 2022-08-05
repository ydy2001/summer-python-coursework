from Core.CoreTask import *
from Core.CoreEnum import *
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QPushButton

class TaskSmallWidget(QWidget):
    def __init__(self, task: Task):
        super().__init__()
        self.task = task
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        
        # (ruilin) text 是用户所看到的界面, 用 to_string 方法来获取
        text = self.task.to_string()

        self.label = QLabel(text=text, parent=self)
        self.del_but = QPushButton(text='删除', parent=self)

        self.main_layout.addWidget(self.label, 0, 0, 1, 5)
        self.main_layout.addWidget(self.del_but, 0, 5, 1, 1)
