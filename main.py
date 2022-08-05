# 图形化界面的入口
# (Blame) Ruilin Who
# CoAuthor: Ydy --- ydy2001@buaa.edu.cn

from multiprocessing.sharedctypes import Value
import sys
import time
from Core import CoreTask, CoreSchedule
from Core.CoreEnum import ImportanceLevel
from Bridge import BridgeTaskSmallWidget
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QMainWindow,
    QLineEdit,      # 输入框 
    QPushButton,    # 按钮
    QTextEdit,
    QAction,        # 点击菜单所对应的行为
    QLabel,
    QScrollArea,
    QMessageBox,    # 消息框
)
from PyQt5.QtWidgets import (
    QGridLayout,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt

class MainUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # 由于beta版限制，在此声明 self.schedule
        self.schedule = CoreSchedule.Schedule()
        self.setup_UI()
        self.setup_input_task_logic()

    # 从总体上将主窗口分成左右两个部分
    def set_right_left(self):
        # 设置主窗口
        self.main_window = QWidget()
        self.main_window_layout = QGridLayout()
        self.main_window.setLayout(self.main_window_layout)
        # 设置左窗口
        self.left_window = QWidget()
        self.left_window_layout = QGridLayout()
        self.left_window.setLayout(self.left_window_layout)
        # 设置右窗口
        self.right_window = QWidget()
        self.right_window_layout = QGridLayout()
        self.right_window.setLayout(self.right_window_layout)
        # 合并左右窗口至主窗口
        self.main_window_layout.addWidget(self.left_window, 0, 0, 30, 1)
        self.main_window_layout.addWidget(self.right_window, 0, 1, 30, 7)
        # 设置主窗口为最终显示窗口
        self.setCentralWidget(self.main_window)

    # 填左半部分
    def fill_left(self):
        self.left_button0 = QPushButton("月历模式")
        self.left_button1 = QPushButton("重要性模式")
        self.left_window_layout.addWidget(self.left_button0, 0, 0, 1, 1)
        self.left_window_layout.addWidget(self.left_button1, 1, 0, 1, 1)

    # 填右半部分
    def fill_right(self):
        self.set_right_input_window() # 综合了输入信息的小窗口
        #self.set_right_task_list()    # 设置当日任务展示列表

    # 设置用于新建任务的小窗口
    def set_right_input_window(self):
        
        # 依次设置每个Task信息的输入
        # 标题
        self.title_input_label = QLabel('标题: ')
        self.title_input_line = QLineEdit()
        self.title_input_line.setPlaceholderText('请输入标题，默认为 untitled')
        self.right_window_layout.addWidget(self.title_input_label,
                                                 0, 0, 1, 1)
        self.right_window_layout.addWidget(self.title_input_line,
                                                 0, 1, 1, 5)
        # ddl
        self.ddl_input_label = QLabel('截止时间: ')
        self.ddl_input_line = QLineEdit()
        self.ddl_input_line.setPlaceholderText('请输入截止时间，格式如 2022-01-01 23:59，默认为无截止时间')
        self.right_window_layout.addWidget(self.ddl_input_label,
                                                 1, 0, 1, 1)
        self.right_window_layout.addWidget(self.ddl_input_line,
                                                 1, 1, 1, 5)
        # start_time
        self.start_time_input_label = QLabel('开始时间: ')
        self.start_time_input_line = QLineEdit()
        self.start_time_input_line.setPlaceholderText('请输入任务开始时间，格式如2022-01-01 23:59，默认为当前系统时间')
        self.right_window_layout.addWidget(self.start_time_input_label,
                                                 2, 0, 1, 1)
        self.right_window_layout.addWidget(self.start_time_input_line,
                                                 2, 1, 1, 5)
        # importance_level
        self.importance_level_input_label = QLabel('重要程度: ')
        self.importance_level_input_line = QLineEdit()
        self.importance_level_input_line.setPlaceholderText('请输入数字 0 - 4，数字越大代表该任务越重要')
        self.right_window_layout.addWidget(self.importance_level_input_label,
                                                 3, 0, 1, 1)
        self.right_window_layout.addWidget(self.importance_level_input_line,
                                                 3, 1, 1, 5)
        # tag
        self.tag_input_label = QLabel('任务标签: ')
        self.tag_input_line = QLineEdit()
        self.tag_input_line.setPlaceholderText('请设定任务标签，默认为 uncategorized')
        self.right_window_layout.addWidget(self.tag_input_label,
                                                 4, 0, 1, 1)
        self.right_window_layout.addWidget(self.tag_input_line,
                                                 4, 1, 1, 5)
        # content
        self.content_input_label = QLabel('任务内容: ')
        self.content_input_line = QTextEdit()
        self.content_input_line.setPlaceholderText('请输入任务内容')
        self.right_window_layout.addWidget(self.content_input_label,
                                                 5, 0, 1, 1)
        self.right_window_layout.addWidget(self.content_input_line,
                                                 5, 1, 3, 5)
        # remark
        self.remark_input_label = QLabel('备注: ')
        self.remark_input_line = QTextEdit()
        self.remark_input_line.setPlaceholderText('请输入备注')
        self.right_window_layout.addWidget(self.remark_input_label,
                                                 8, 0, 1, 1)
        self.right_window_layout.addWidget(self.remark_input_line,
                                                 8, 1, 2, 5)
        
        # 设置确认新建任务按钮
        self.right_input_button = QPushButton("确认新建任务")
        self.right_input_button.setFixedSize(200, 220)
        self.right_window_layout.addWidget(self.right_input_button,
                                                 0, 6, 5, 1)
        
        # (ruilin) 以下是原来的函数 set_right_task_list 中的内容
        self.right_task_list_window = QWidget()
        self.right_task_list_window_layout = QVBoxLayout()
        self.right_task_list_window.setLayout(self.right_task_list_window_layout)
        # 设置滚动
        self.task_list_scroll = QScrollArea(self.right_window)
        self.task_list_scroll.setWidget(self.right_task_list_window)
        self.task_list_scroll.setWidgetResizable(True)
        self.right_window_layout.addWidget(self.task_list_scroll, 10, 0, 20, 7)

        # 显示滚动区中的任务内容
        self.show_task(time.strftime("%Y-%m-%d", time.localtime()), False)

    def setup_UI(self):
        self.setWindowTitle('AweSomeSchedule')
        self.resize(1500, 1400)
        self.set_right_left()
        self.fill_left()
        self.fill_right()

    def setup_input_task_logic(self):
        # (ruilin) “确认新建任务” 按钮作为信号，链接到槽 “generate_task” 中
        self.right_input_button.clicked.connect(self.generate_task)

    # <关于展示任务>==========================================================================
    
    # 显示某用户某一天的日程，当前版本date, user参数尚未被使用
    def show_task(self, date, user):
        # 排序
        self.schedule.sort_by_ddl()
        # 清空当前 task_list_window 中的对象
        item_list = list(range(self.right_task_list_window_layout.count()))
        item_list.reverse()
        for i in item_list:
            item = self.right_task_list_window_layout.itemAt(i)
            self.right_task_list_window_layout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
        #####################################
        for _ in self.schedule.tasks:
            temp = BridgeTaskSmallWidget.TaskSmallWidget(_)
            self.right_task_list_window_layout.addWidget(temp)

    def generate_task(self):
        # (ruilin) 已添加异常判断和默认值

        # (ruilin) 截止时间
        try:
            ddl = self.ddl_input_line.text()
            if len(ddl) == 0:
                ddl = '2077-12-31 23:59'
            time.strptime(ddl, "%Y-%m-%d %H:%M")
        except ValueError:
            self.show_failure_msg('截止时间格式错误', '时间格式为:\nYYYY-MM-DD hh:mm')
            return

        # (ruilin) 标题及默认值
        title = self.title_input_line.text()
        if len(title) == 0: title = 'untitled'

        # (ruilin) 内容和备注，这两个值可以为空
        content = self.content_input_line.toPlainText()
        remark = self.remark_input_line.toPlainText()

        # (ruilin) 开始时间
        try:
            start_time = self.start_time_input_line.text()
            if len(start_time) == 0:
                start_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
            time.strptime(start_time, "%Y-%m-%d %H:%M")
        except ValueError:
            self.show_failure_msg('开始时间格式错误', '时间格式为:\nYYYY-MM-DD hh:mm')
            return

        # (ruilin) 重要性级别，默认为 0
        importance_level = self.importance_level_input_line.text()
        if len(importance_level) == 0:
            importance_level = ImportanceLevel.INSIGNIFICANT
        else:
            importance_level = ImportanceLevel(int(importance_level))
        
        # (ruilin) 将 task 添加到 self.schedule
        task = CoreTask.Task(ddl, title, content, remark, start_time, importance_level)
        self.schedule.add_task(task=task)
        self.show_task(False, False) # date, user 参数暂时无用
    
    # (ruilin) utils: 该函数根据输入的标题和文字显示对应“错误消息框”
    def show_failure_msg(self, title:str, text:str) -> None:
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
    main_ui = MainUI()
    main_ui.show()
    sys.exit(app.exec_())
