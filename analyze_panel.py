# ===============================================================
# (blame) ruilin
# 分析模式
# ===============================================================

import os
import sys
import json
import datetime
import calendar
from calendar import month

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
    QGridLayout,    # 网格状布局
    QSizePolicy,
    QSpinBox,
    QDialog,
    QVBoxLayout,
    QScrollArea,
)
from matplotlib import widgets
from Bridge.BridgeTaskSmallWidget import *
from Core.CoreSchedule import *


class analyze_panel(QWidget):

    def __init__(self, Username:str = 'rlh'):
        super().__init__()
        self.resize(2000, 1500)
        self.panel_layout = QGridLayout() # 网格内部通过网格布局来实现
        self.setLayout(self.panel_layout)

        print(Username)
        # (ruilin) 分析常规任务
        txt = '到目前为止：\n\n'

        if os.path.exists('.as/' + Username + '_history') and \
           os.path.getsize('.as/' + Username + '_history') != 0:
            
            with open('.as/' + Username + '_history', 'r') as f:
                sch1 = load_schedule_from_list(json.load(f))
                lst1 = sch1.to_dict()
                if len(lst1) != 0:
                    txt += '你已经完成了 <{}> 个普通任务 ~\n'.format(len(lst1))

                    txt += '这些普通任务中包括: <{}> 个紧急任务，<{}> 个重要任务, <{}> 个值得关注的任务, \n'.format(
                        len([tsk for tsk in lst1 if tsk['importance_level'] == ImportanceLevel.URGENT]),
                        len([tsk for tsk in lst1 if tsk['importance_level'] == ImportanceLevel.IMPORTANT]),
                        len([tsk for tsk in lst1 if tsk['importance_level'] == ImportanceLevel.NOTE_WORTHY])
                    )

                    txt += '另外，你还完成了 <{}> 个普通的任务和 <{}> 个无关紧要的任务.'.format(
                        len([tsk for tsk in lst1 if tsk['importance_level'] == ImportanceLevel.NORMAL]),
                        len([tsk for tsk in lst1 if tsk['importance_level'] == ImportanceLevel.INSIGNIFICANT])
                    )
                    txt += '\n'

        max_continue_days = -1
        max_continue_task = None
        min_continue_days = 114514
        min_continue_task = None


        if os.path.exists('.as/' + Username) and \
            os.path.getsize('.as/' + Username) != 0:
            with open('.as/' + Username, 'r') as f:
                sch2 = load_schedule_from_list(json.load(f))
                lst2 = sch2.to_dict()
                

                daily_num = len([tsk for tsk in sch2.tasks if tsk.tasktype == Task_type.DAILY])
                txt += '\n努力的你，给自己布置了 <{}> 个每日任务.\n'.format(daily_num)

                for tsk in sch2.tasks:
                    if tsk.tasktype == Task_type.DAILY:

                        # (ruilin) interval 保存开始和结束之间的天数
                        et = datetime.datetime(*tsk.ddl_year_and_month())
                        st = datetime.datetime(*tsk.start_year_and_month())
                        interval = (et - st).days + 1
                        finisheddays = tsk.count_finished_days()

                        txt += '对于进行中的每日任务 <{}>， 你总共有 <{}> 天的计划，已经完成了 <{}> 天，打卡率为 <{}%>. \n'.format(
                            tsk.title, interval, finisheddays, 100.0 * finisheddays / interval
                        )

                        if finisheddays > max_continue_days:
                            max_continue_days = finisheddays
                            max_continue_task = tsk
                        if finisheddays < min_continue_days:
                            min_continue_days = finisheddays
                            min_continue_task = tsk


        if os.path.exists('.as/' + Username + '_expired') and \
            os.path.getsize('.as/' + Username + '_expired') != 0:
            with open('.as/' + Username + '_expired', 'r') as f:
                sch3 = load_schedule_from_list(json.load(f))
                lst3 = sch3.to_dict()
                

                expired_num = len([tsk for tsk in sch3.tasks if tsk.status == TaskStatus.EXPIRED])
                txt += '\n时间不等人，你有 <{}> 个任务已经过期了.'.format(expired_num)

                if len([tsk for tsk in sch3.tasks if tsk.tasktype == Task_type.DAILY]) != 0:
                    txt += '\n\n在过期的任务中，有一些是已经结束了的每日任务规划：\n'
                for tsk in sch3.tasks:
                    if tsk.tasktype == Task_type.DAILY:
                        et = datetime.datetime(*tsk.ddl_year_and_month())
                        st = datetime.datetime(*tsk.start_year_and_month())
                        interval = (et - st).days + 1
                        finisheddays = tsk.count_finished_days()

                        txt += '对于已经结束了的每日任务 <{}>， 你总共有 <{}> 天的计划，一共完成了 <{}> 天，打卡率为 <{}%>. \n'.format(
                            tsk.title, interval, finisheddays, 100.0 * finisheddays / interval
                        )

                        
                        if finisheddays > max_continue_days:
                            max_continue_days = finisheddays
                            max_continue_task = tsk
                        if finisheddays < min_continue_days:
                            min_continue_days = finisheddays
                            min_continue_task = tsk

        if max_continue_task:
            txt += '\n你坚持得最久的每日任务是 <{}>，至少坚持了 <{}> 天！'.format(max_continue_task.title, max_continue_days)
            txt += '\n你坚持得最短的每日任务是 <{}>，它只坚持了 <{}> 天 QAQ\n'.format(min_continue_task.title, min_continue_days)

        
        self.lb = QLabel(txt)
        self.panel_layout.addWidget(self.lb, 0, 0, 10, 10)

        self.happy_button = QPushButton('开心')
        self.panel_layout.addWidget(self.happy_button, 11, 0, 1, 1)
        self.happy_button.clicked.connect(self.happy_triggered)

        self.sad_button = QPushButton('难过')
        self.panel_layout.addWidget(self.sad_button, 11, 1, 1, 1)
        self.sad_button.clicked.connect(self.sad_triggered)
        
    def happy_triggered(self):
        self.show_msg('^_^', '啦啦啦，好开心呀 😊')
    
    def sad_triggered(self):
        self.show_msg('ToT', '不要难过，继续努力吧 😗') 

    def show_msg(self, title:str, text:str) -> None:
        msgbox = QMessageBox()
        msgbox.setWindowTitle(title)
        msgbox.setText(text)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setStyleSheet('''QLabel{min-width:300px; min-height:150px}''')
        msgbox.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = analyze_panel()
    ui.show()
    sys.exit(app.exec_())

