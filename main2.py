# 图形化界面的入口
# (Blame) Ruilin Who
# CoAuthor: Ydy --- ydy2001@buaa.edu.cn

import os
import time
import json


from month_lendar import *
from Core import CoreTask, CoreSchedule
from Core.CoreEnum import *
from Core.CoreArgorithm import *
from Bridge import BridgeTaskSmallWidget, BridgeTaskBigWIdget
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
    QInputDialog,
    QDialog,        # 对话输入框
    QSizePolicy,
    QGridLayout,
    QVBoxLayout,
    QDateEdit,
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPalette, QColor

class MainUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.schedule = CoreSchedule.Schedule()
        self.current_user = 'default user'
        ## showing_big_widget 为当前在 detail window 中展示的 TaskBigWidget
        self.showing_big_widget = None
        self.setup_UI()

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
        # 合并左至主窗口
        # (ruilin) 原来的传统模式窗口已经被移动到 fill_right 函数中
        self.main_window_layout.addWidget(self.left_window, 0, 0, 30, 1)
        # 设置主窗口为最终显示窗口
        self.setCentralWidget(self.main_window)
        

    # 填左半部分
    def fill_left(self):

        # (ruilin) 默认时 UI 为传统模式
        self.current_UI_mode = UI_mode.TRADITIONAL

        # (ruilin) 
        # 用户相关
        self.user_label = QLabel('当前用户: ' + self.current_user)
        self.left_window_layout.addWidget(self.user_label, 0, 0, 1, 2)
        self.change_user_but = QPushButton('切换用户')
        self.left_window_layout.addWidget(self.change_user_but, 1, 0, 1, 2)


        self.left_button0 = QPushButton('月历模式')
        self.left_window_layout.addWidget(self.left_button0, 2, 0, 1, 1)
        self.left_button0.clicked.connect(self.month_calendar_triggered)

        self.left_button1 = QPushButton('传统模式')
        self.left_window_layout.addWidget(self.left_button1, 2, 1, 1, 1)
        self.left_button1.clicked.connect(self.traditional_triggered)

        self.whatever_label = QLabel("")
        self.left_window_layout.addWidget(self.whatever_label, 3, 0, 10 , 1)

        # (ruilin) 给控制栏设置灰色背景以进行强调
        plt = self.left_window.palette()
        plt.setColor(QPalette.Background, QColor(224, 224, 224))
        self.left_window.setPalette(plt)
        self.left_window.setAutoFillBackground(True)
        # (ruilin) self.set_left_logic
        

    # 填右半部分
    # (ruilin) fill_right 可能有歧义
    # (ruilin) 在新版本中，它将会构造并创建一个新的传统模式窗口
    def fill_right(self):

        # 设置右窗口
        self.right_window = QWidget()
        self.right_window_layout = QGridLayout()
        self.right_window.setLayout(self.right_window_layout)
        # 合并右窗口至主窗口
        self.main_window_layout.addWidget(self.right_window, 0, 1, 30, 16)

        self.set_right_manipulation_window()  # (ruilin) 关于排序的小器件
        self.set_right_input_window() # 综合了输入信息的小窗口


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
        self.right_input_button = QPushButton("新建普通任务")
        self.right_input_button.setMinimumHeight(100)
        self.right_window_layout.addWidget(self.right_input_button,
                                                 10, 1, 2, 4)

        self.right_input_daily_button = QPushButton("新建每日任务")
        self.right_input_daily_button.setMinimumHeight(100)
        self.right_window_layout.addWidget(self.right_input_daily_button,
                                                 10, 5, 2, 1)
        
        # (ruilin) 以下是原来的函数 set_right_task_list 中的内容
        self.right_task_list_window = QWidget()
        self.right_task_list_window_layout = QVBoxLayout()
        self.right_task_list_window.setLayout(self.right_task_list_window_layout)
        # 设置滚动
        self.task_list_scroll = QScrollArea(self.right_window)
        self.task_list_scroll.setWidget(self.right_task_list_window)
        self.task_list_scroll.setWidgetResizable(True)
        self.right_window_layout.addWidget(self.task_list_scroll, 0, 6, 30, 10)

        # 显示滚动区中的任务内容
        self.show_task(begindate=self.begin_dateedit.date(),
                       enddate=self.end_dateedit.date())

        # 在初始化 右半部分窗口的时候，将逻辑链接到槽中
        self.setup_input_task_logic()


    def set_right_manipulation_window(self):

        # 排序功能
        self.arrange_label = QLabel('<整理日程>')
        self.right_window_layout.addWidget(self.arrange_label, 12, 0, 2, 1)

        policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.arrange_ddl_but = QPushButton('按DDL整理')
        self.arrange_ddl_but.setSizePolicy(policy)
        self.arrange_tag_but = QPushButton('按任务标签整理')
        self.arrange_tag_but.setSizePolicy(policy)
        self.arrange_title_but = QPushButton('按标题整理')
        self.arrange_title_but.setSizePolicy(policy)
        self.arrange_importance_but = QPushButton('按重要程度整理')
        self.arrange_importance_but.setSizePolicy(policy)
        ## 排序功能的小窗口
        self.arrange_window = QWidget()
        self.arrange_layout = QGridLayout()
    
        self.arrange_window.setLayout(self.arrange_layout)
        self.arrange_layout.addWidget(self.arrange_ddl_but, 0, 0, 1, 1)
        self.arrange_layout.addWidget(self.arrange_tag_but, 0, 1, 1, 1)
        self.arrange_layout.addWidget(self.arrange_title_but, 1, 0, 1, 1)
        self.arrange_layout.addWidget(self.arrange_importance_but, 1, 1, 1, 1)
        self.right_window_layout.addWidget(self.arrange_window, 12, 1, 3, 5)

        # (ruilin) set_arrange_logic
        self.arrange_ddl_but.clicked.connect(self.arrange_triggered)
        self.arrange_importance_but.clicked.connect(self.arrange_triggered)
        self.arrange_title_but.clicked.connect(self.arrange_triggered)
        self.arrange_tag_but.clicked.connect(self.arrange_triggered)

        # (ruilin) 以下使用日历对话框器件
        self.begin_dateedit = QDateEdit(QDate.currentDate())
        self.begin_dateedit.setCalendarPopup(True)
        self.begin_dateedit.setDisplayFormat('开始: yyyy-MM-dd')
        self.arrange_layout.addWidget(self.begin_dateedit, 2, 0, 1, 1)

        self.end_dateedit = QDateEdit(QDate(2077, 12, 31))
        self.end_dateedit.setCalendarPopup(True)
        self.end_dateedit.setDisplayFormat('结束: yyyy-MM-dd')
        self.arrange_layout.addWidget(self.end_dateedit, 2, 1, 1, 1)

        self.begin_dateedit.dateChanged.connect(self.datechange_triggered)
        self.end_dateedit.dateChanged.connect(self.datechange_triggered)

    def setup_UI(self):
        self.setWindowTitle('AweSomeSchedule')
        self.resize(2400, 1500)
        self.set_right_left()   # (ruilin) 将主界面分为 [控制按钮|工作面板] 两部分
        self.fill_left()        # (ruilin) 初始化控制按钮
        self.fill_right()       # (ruilin) 初始化一开始的添加界面

    def setup_input_task_logic(self):
        # (ruilin) “确认新建任务” 按钮作为信号，链接到槽 “generate_task” 中
        ## 现链接到槽 generate_task_shell 中
        self.right_input_button.clicked.connect(self.generate_task_shell)
        self.right_input_daily_button.clicked.connect(self.generate_task_shell)

    def generate_task_shell(self):

        if self.sender() == self.right_input_button:
            tasktype = Task_type.NORMAL
        else:
            tasktype = Task_type.DAILY

        self.generate_task(self.ddl_input_line.text(),
                           self.title_input_line.text(),
                           self.content_input_line.toPlainText(),
                           self.remark_input_line.toPlainText(),
                           self.start_time_input_line.text(),
                           self.importance_level_input_line.text(),
                           self.tag_input_line.text(),
                           tasktype = tasktype)

    # <关于展示任务>==========================================================================

    def arrange_triggered(self):
        if self.sender() == self.arrange_ddl_but:
            self.show_task(func=cmp_by_ddl, begindate=self.begin_dateedit.date(),
                           enddate=self.end_dateedit.date())
        elif self.sender() == self.arrange_importance_but:
            self.show_task(func=cmp_by_importance, begindate=self.begin_dateedit.date(),
                           enddate=self.end_dateedit.date())
        elif self.sender() == self.arrange_tag_but:
            self.show_task(func=cmp_by_tag, begindate=self.begin_dateedit.date(),
                           enddate=self.end_dateedit.date())
        elif self.sender() == self.arrange_title_but:
            self.show_task(func=cmp_by_title, begindate=self.begin_dateedit.date(),
                           enddate=self.end_dateedit.date())

    def datechange_triggered(self):
        begintime = self.begin_dateedit.date()
        endtime = self.end_dateedit.date()
        self.show_task(begindate = begintime, enddate = endtime)

    def clear_layout(self, layout):
        item_list = list(range(layout.count()))
        item_list.reverse()
        for i in item_list:
            item = layout.itemAt(i)
            layout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()

    # 更加泛化的 delete_task
    # 其中 trick 参数用于决定是否关联性地删除当前显示的任务
    def delete_task(self, task: CoreTask.Task):
        self.schedule.remove_designated_task(task)
        self.show_task(begindate=self.begin_dateedit.date(),
                       enddate=self.end_dateedit.date())
    
    # (ruilin) <每日任务专用> 彻底删除某个任务
    def trigger_fully_delete_task(self):
        self.delete_task(self.sender().parent().task)

    # (ruilin) 新的点击删除按钮的槽函数
    def trigger_delete_task(self):
        cur_tsk = self.sender().parent().task
        if cur_tsk.tasktype == Task_type.NORMAL:
            self.delete_task(self.sender().parent().task)
        else:
            cur_tsk.set_someday_finished(datetime.datetime.today().date()) # (ruilin) 放进去了一个datetime对象
            self.show_task(begindate=self.begin_dateedit.date(),
                       enddate=self.end_dateedit.date())


    # 显示某用户某一天的日程，当前版本date, user参数尚未被使用
    def show_task(self, 
                  store = True,
                  func = cmp_by_ddl, 
                  begindate = None, 
                  enddate = None):
            
        # 排序
        self.schedule.sort_task(cmp_func=func)
        # 清空当前 task_list_window 中的对象
        self.clear_layout(self.right_task_list_window_layout)

        # (ruilin) 将 schedule 中的每个 Task 使用一个Widget进行展示
        # (ruilin) 先处理每日任务
        today = datetime.datetime.today().date()
        for _ in self.schedule.tasks:
            if _.tasktype != Task_type.DAILY: continue
            if _.check_someday_if_finished(today): continue
            if begindate and enddate:
                tskdate = QDate(*_.ddl_year_and_month())
                if tskdate < begindate or tskdate > enddate: continue

            print('today = ', today)

            temp = BridgeTaskSmallWidget.TaskSmallWidget(_)
            temp.del_but.clicked.connect(self.trigger_delete_task)
            temp.detail_but.clicked.connect(self.show_task_settings_dialog)
            temp.fully_delete_but.clicked.connect(self.trigger_fully_delete_task)
            self.right_task_list_window_layout.addWidget(temp)
        
        # (ruilin) 再处理普通任务
        for _ in self.schedule.tasks:
            if _.tasktype != Task_type.NORMAL: continue
            if begindate and enddate:
                tskdate = QDate(*_.ddl_year_and_month())
                if tskdate < begindate or tskdate > enddate: continue

            temp = BridgeTaskSmallWidget.TaskSmallWidget(_)
            temp.del_but.clicked.connect(self.trigger_delete_task)
            temp.detail_but.clicked.connect(self.show_task_settings_dialog)
            self.right_task_list_window_layout.addWidget(temp)


        # (ruilin) 设计为从上到下的布置，不会让 Task 一开始显示在中间
        if len(self.schedule.tasks) < 6:
            for i in range(6 - len(self.schedule.tasks)):
                temp = QLabel()
                self.right_task_list_window_layout.addWidget(temp)
        
        # (ruilin) 每次调用 show_task 的时候，都会重新刷新本地数据
        if store:
            # make sure user file exists
            path = '.as/' + self.current_user
            if not os.path.exists(path):
                temp = open(path, 'w')
                temp.close()
            with open(path, 'w') as f:
                # print('Dict = ', self.schedule.to_dict())
                json.dump(self.schedule.to_dict(), f)

    # (ruilin) 该函数是基本功能的使能函数，作用是在程序中添加一个指定的任务
    def generate_task(self : str, 
                      _ddl : str,
                      _title : str,
                      _content : str, 
                      _remark : str, 
                      _start_time : str, 
                      _importance_level : str, 
                      _tag : str,
                      tasktype : Task_type,
                      check_only = False):
        # (ruilin) 已添加异常判断和默认值
        ## 修复了忘记处理tag的bug
        ## 修复了importance_level异常值判断的问题
        ## 更改为重用性更高的版本
        ## 增加了返回值：成功时返回生成的 task 或 Ture，出错时返回False
        ## 增加了参数 check_only，当其被设为True，本函数将只进行参数检查，不实际生成任务

        # (ruilin) 截止时间
        try:
            ddl = _ddl
            if len(ddl) == 0:
                ddl = '2077-12-31 23:59'
            time.strptime(ddl, "%Y-%m-%d %H:%M")
        except ValueError:
            self.show_failure_msg('截止时间格式错误', '时间格式为:\nYYYY-MM-DD hh:mm')
            return False

        # (ruilin) 标题及默认值
        title = _title
        if len(title) == 0: title = 'untitled'

        # (ruilin) 内容和备注，这两个值可以为空
        content = _content
        remark = _remark

        # (ruilin) 开始时间
        try:
            start_time = _start_time
            if len(start_time) == 0:
                start_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
            time.strptime(start_time, "%Y-%m-%d %H:%M")
        except ValueError:
            self.show_failure_msg('开始时间格式错误', '时间格式为:\nYYYY-MM-DD hh:mm')
            return False

        # (ruilin) 重要性级别，默认为 0
        importance_level = str(_importance_level)
        if len(importance_level) == 0:
            importance_level = ImportanceLevel.INSIGNIFICANT
        else:
            ## 添加非法值判断
            try:
                importance_level = int(importance_level)
                if importance_level < 0 or importance_level > 4:
                    self.show_failure_msg('重要程度输入错误', '请输入0~4之间的整数')
                    return False
                importance_level = ImportanceLevel(int(importance_level))
            except ValueError:
                self.show_failure_msg('重要程度输入错误', '请输入0~4之间的整数')
                return False

        ## tag
        tag = _tag
        if len(tag) == 0: tag = 'uncategorized'

        if check_only == False:
            # (ruilin) 将 task 添加到 self.schedule
            task = CoreTask.Task(ddl, title, content, remark, \
                start_time, importance_level, tag, tasktype = tasktype)
            self.schedule.add_task(task = task)
            self.show_task(begindate=self.begin_dateedit.date(),
                           enddate=self.end_dateedit.date())
            return task
        else:
            return True
    
    # (ruilin) utils: 该函数根据输入的标题和文字显示对应“错误消息框”
    def show_failure_msg(self, title:str, text:str) -> None:
        msgbox = QMessageBox()
        msgbox.setWindowTitle(title)
        msgbox.setText(text)
        # (ruilin) 显示一个图标，不过不太美观，暂时不使用
        # msgbox.setIcon(QMessageBox.Critical) 
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setStyleSheet('''QLabel{min-width:300px; min-height:150px}''')
        msgbox.exec()

    # (ruilin) 新的任务详细信息的UI，弹出一个框，可以显示也可以修改
    def show_task_settings_dialog(self):
        
        # (ruilin) self.dialog 的 parent 是相应的BridgeTaskSmallWidget，这样做是为了找到对应的task
        self.dialog = QDialog(parent=self.sender().parent())
        self.dialog.setWindowTitle('任务详细信息')
        self.dialog.resize(1000, 800)
        # (ruilin) 设置对话框布局
        self.dialog_layout = QGridLayout()
        self.dialog.setLayout(self.dialog_layout)

        tsk = self.sender().parent().task
        # (ruilin) 截止时间 label & lineEdit
        self.cur_ddl_input = QLineEdit(tsk.ddl)
        self.dialog_layout.addWidget(self.cur_ddl_input, 1, 1, 1, 2)
        self.cur_ddl_label = QLabel("\t截止时间")
        self.dialog_layout.addWidget(self.cur_ddl_label, 1, 0, 1, 1)

        # (ruilin) 开始时间 label & lineEdit
        self.cur_starttime_input = QLineEdit(tsk.start_time)
        self.dialog_layout.addWidget(self.cur_starttime_input, 2, 1, 1, 2)
        self.cur_starttime_label = QLabel("\t开始时间")
        self.dialog_layout.addWidget(self.cur_starttime_label, 2, 0, 1, 1)

        # (ruilin) 重要程度 label & lineEdit
        self.cur_importance_input = QLineEdit(str(Importance_to_int[tsk.importance_level]))
        self.dialog_layout.addWidget(self.cur_importance_input, 3, 1, 1, 2)
        self.cur_importance_label = QLabel("\t重要程度")
        self.dialog_layout.addWidget(self.cur_importance_label, 3, 0, 1, 1)


        # (ruilin) 任务标签 label & lineEdit
        self.cur_tag_input = QLineEdit(tsk.tag)
        self.dialog_layout.addWidget(self.cur_tag_input, 4, 1, 1, 2)
        self.cur_tag_label = QLabel("\t任务标签")
        self.dialog_layout.addWidget(self.cur_tag_label, 4, 0, 1, 1)

        # (ruilin) 任务内容 label & lineEdit
        self.cur_content_input = QLineEdit(tsk.content)
        self.cur_content_input.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.dialog_layout.addWidget(self.cur_content_input, 5, 1, 3, 2)
        self.cur_content_label = QLabel("\t任务内容")
        self.dialog_layout.addWidget(self.cur_content_label, 5, 0, 1, 1)

        # (ruilin) 任务备注 label & lineEdit
        self.cur_remark_input = QLineEdit(tsk.remark)
        self.dialog_layout.addWidget(self.cur_remark_input, 8, 1, 3, 2)
        self.cur_remark_input.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.cur_remark_label = QLabel("\t任务备注")
        self.dialog_layout.addWidget(self.cur_remark_label, 8, 0, 1, 1)

        self.ok_button = QPushButton('确定')
        self.dialog_layout.addWidget(self.ok_button, 11, 1, 1, 1)
        self.ok_button.clicked.connect(self.dialog_ok_func)

        self.cancel_button = QPushButton('取消')
        self.dialog_layout.addWidget(self.cancel_button, 11, 2, 1, 1)
        self.cancel_button.clicked.connect(self.dialog_cancel_func)

        self.dialog.exec_()

    # (ruilin) 任务详情对话框点击 OK 后将进行属性修改
    # (ruilin) 这里也是把显示详细属性和修改详细属性合并到一起了
    def dialog_ok_func(self):
        tsk = self.sender().parent().parent().task
        temp_args = (
            self.cur_ddl_input.text(),
            tsk.title,
            self.cur_content_input.text(),
            self.cur_remark_input.text(),
            self.cur_starttime_input.text(),
            self.cur_importance_input.text(),
            self.cur_tag_input.text()
        )

        if self.generate_task(*temp_args, check_only = True):
            self.delete_task(tsk)
            self.generate_task(*temp_args, check_only = False)
            self.dialog.close()

    # (ruilin) 任务详情对话框点击 cancle 后直接关闭
    def dialog_cancel_func(self):
        self.dialog.close()

    # <月历模式> 相关函数 =====================================================================

    # (ruilin) 不知道为啥，需要用这个函数来请理 Layout
    def clear_layout(self, layout):
        item_list = list(range(layout.count()))
        item_list.reverse()
        for i in item_list:
            item = layout.itemAt(i)
            layout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()

    # (ruilin) 切换到月历模式.
    # (ruilin) 点击月历模式后，需要请理原来的 layout
    def month_calendar_triggered(self):

        # (ruilin) 如果 UI 模式已经在月历模式下，不做任何操作
        if self.current_UI_mode == UI_mode.CALANDAR: return
        self.current_UI_mode = UI_mode.CALANDAR

        self.clear_layout(self.right_window_layout)
        self.month_calander = Monthlendar(self.schedule)
        self.main_window_layout.addWidget(self.month_calander, 0, 1, 30, 16)


    # (ruilin) 切换到传统模式
    def traditional_triggered(self):

        if self.current_UI_mode == UI_mode.TRADITIONAL: return
        self.current_UI_mode = UI_mode.TRADITIONAL

        self.clear_layout(self.month_calander.month_lendar_layout)
        self.main_window_layout.removeWidget(self.month_calander)
        self.fill_right()

user_name = 'Administrator_ruilin'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_ui = MainUI()
    main_ui.show()
    sys.exit(app.exec_())
