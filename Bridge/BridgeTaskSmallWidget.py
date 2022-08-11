from Core.CoreTask import *
from Core.CoreEnum import *
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QPushButton
from PyQt5 import QtGui
from PyQt5.QtGui import QPalette, QColor

TaskStatus_to_color = {
    TaskStatus.DELETED : '#eb4034',   
    TaskStatus.EXPIRED : '#3d613d',       
    TaskStatus.DONE : '#8a1374',       
    TaskStatus.NOT_STARTED : '#E66832',     
    TaskStatus.IN_PROCESS : '#3274E6',  
}

class TaskSmallWidget(QWidget):
    def __init__(self, task: Task):
        super().__init__()
        self.task = task
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        
        # (ruilin) text 是用户所看到的界面, 用 to_string 方法来获取
        self.text = self.task.to_string()

        # (ruilin) label 及初始值
        self.label = QLabel(parent=self)
        self.label.setText("<font color=%s>%s</font>" % \
            (TaskStatus_to_color[self.task.status], self.text))

        # (ruilin) 设置 text 字体
        font = QtGui.QFont() 
        font.setFamily('微软雅黑')
        font.setBold(True) 
        font.setPointSize(12)
        font.setWeight(50)
        self.label.setFont(font) 

        self.del_but = QPushButton(
            text = '今日完成' if (task.tasktype == Task_type.DAILY) else '删除', 
            parent = self)
        self.change_state_but = QPushButton(text='切换状态', parent=self)
        self.detail_but = QPushButton(text='查看任务详情', parent=self)

        self.change_state_but.clicked.connect(self.change_state_triggered)

        # (ruilin) 关于每日任务和普通任务的布局
        # (ruilin) 这里没写好，其实最好还是分为两个Widget
        if self.task.tasktype == Task_type.DAILY:
            self.main_layout.addWidget(self.label, 0, 0, 2, 5)

            self.fully_delete_but = QPushButton(text = '彻底删除', parent = self)
            self.main_layout.addWidget(self.fully_delete_but, 0, 5, 1, 1)

            self.main_layout.addWidget(self.del_but, 0, 6, 1, 1)
            self.main_layout.addWidget(self.change_state_but, 1, 5, 1, 1)
            self.main_layout.addWidget(self.detail_but, 1, 6, 1, 1)
        else:
            self.main_layout.addWidget(self.label, 0, 0, 1, 4)
            self.main_layout.addWidget(self.del_but, 0, 4, 1, 1)
            self.main_layout.addWidget(self.change_state_but, 0, 5, 1, 1)
            self.main_layout.addWidget(self.detail_but, 0, 6, 1, 1)

        # (ruilin) 每日任务的背景色强调
        if self.task.tasktype == Task_type.DAILY:
            plt = self.palette()
            plt.setColor(QPalette.Background, QColor(182, 211, 227))
            self.setPalette(plt)
            self.setAutoFillBackground(True)

    def change_state_triggered(self):
        new_state = Int_to_TaskStatus[ ( TaskStatus_to_int[self.task.status] + 1 ) % 5 ]
        self.task.status = new_state
        self.text = self.task.to_string()

        self.label.setText("<font color=%s>%s</font>" % \
            (TaskStatus_to_color[self.task.status], self.text))

class TaskSmallWidget_2(QWidget):
    def __init__(self, task: Task):
        super().__init__()
        self.task = task
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        
        text = self.task.to_string()

        self.label = QLabel(text=text, parent=self)
        self.del_but = QPushButton(
            text = '今日完成' if (task.tasktype == Task_type.DAILY) else '删除', 
            parent = self)

        self.main_layout.addWidget(self.label, 0, 0, 1, 5)
        self.main_layout.addWidget(self.del_but, 0, 5, 1, 1)
