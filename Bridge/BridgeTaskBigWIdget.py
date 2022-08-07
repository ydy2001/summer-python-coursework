from Core.CoreTask import *
from Core.CoreEnum import *
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, QHBoxLayout


class TaskBigWidget(QWidget):
    def __init__(self, task: Task):
        super().__init__()
        self.task = task
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # set title
        self.title_label = QLabel(task.title)
        self.title_mod_but = QPushButton(text='修改标题', parent=self)
        self.add_h(self.title_label, self.title_mod_but)

        # set importance_level
        self.importance_level_label = QLabel(str(task.importance_level))
        self.importance_level_mod_but = QPushButton(text='修改重要程度', parent=self)
        self.add_h(self.importance_level_label, self.importance_level_mod_but)

        # set tag
        self.tag_label = QLabel('任务标签: ' + self.task.tag)
        self.tag_mod_but = QPushButton(text='修改标签', parent=self)
        self.add_h(self.tag_label, self.tag_mod_but)

        # set ddl
        self.ddl_label = QLabel('DDL: ' + self.task.ddl)
        self.ddl_mod_but = QPushButton(text='修改DDL', parent=self)
        self.add_h(self.ddl_label, self.ddl_mod_but)

        # set content
        self.content_content = QLabel('任务内容: \n' + self.task.content)
        self.content_mod_but = QPushButton(text='修改任务内容', parent=self)
        self.add_h(self.content_content, self.content_mod_but)

        # set remark
        self.remark_content = QLabel('任务备注: \n' + self.task.remark)
        self.remark_mod_but = QPushButton(text='修改任务备注', parent=self)
        self.add_h(self.remark_content, self.remark_mod_but)

    def add_h(self, content: QLabel, but: QPushButton):
        temp_layout = QHBoxLayout()
        temp_widget = QWidget()
        temp_widget.setLayout(temp_layout)
        temp_layout.addWidget(content)
        temp_layout.addWidget(but)
        self.main_layout.addWidget(temp_widget)
