# ===============================================================
# (blame) ruilin
# 月历模式，把 calender 作为一个 Widget 来实现
# ===============================================================

import sys
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
from Core.CoreSchedule import Schedule

# Monthlendar 是我自己创的一个词，指月历
class Monthlendar(QWidget):

    def __init__(self, schedule : Schedule = None):
        super().__init__()
        self.schedule = schedule    # schedule = [task for task in 用户的所有任务]
        # self.resize(2000, 1500)
        self.month_lendar_layout = QGridLayout() # 网格内部通过网格布局来实现
        self.setLayout(self.month_lendar_layout)

        # $(ruilin) 默认的年份, 月份为当前时间
        today = datetime.datetime.today()
        self.current_year = 2077 # today.year
        self.current_month = 12 # today.month

        # $(ruilin) 选择年份
        self.year_spinbox = QSpinBox()
        self.year_spinbox.setRange(2000, 2100)
        self.year_spinbox.setSingleStep(1)
        self.year_spinbox.setValue(self.current_year)
        self.month_lendar_layout.addWidget(self.year_spinbox, 0, 1, 1, 1)

        year_label = QLabel('      选择年份: ')
        self.month_lendar_layout.addWidget(year_label, 0, 0, 1, 1)

        # $(ruilin) 选择月份
        self.month_spinbox = QSpinBox()
        self.month_spinbox.setRange(1, 12)
        self.month_spinbox.setSingleStep(1)
        self.month_spinbox.setValue(self.current_month)
        self.month_lendar_layout.addWidget(self.month_spinbox, 0, 3, 1, 1)

        month_label = QLabel('      选择月份: ')
        self.month_lendar_layout.addWidget(month_label, 0, 2, 1, 1)

        # $(ruilin) 年份或者月份微调的时候，信号链接到相应的处理函数
        self.year_spinbox.valueChanged.connect(self.year__month_changed)
        self.month_spinbox.valueChanged.connect(self.year__month_changed)

        self.widgets = [QPushButton() for i in range(6 * 7)]     # 创建 5行7列的小部件
        self.weekday_widgets = [QWidget() for i in range(7)]     # 7列的小部件，用于显示星期几表示    

        self.button_Adaptive = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        for wg in self.widgets:
            wg.setSizePolicy(self.button_Adaptive)
            wg.setParent(self)

        # $(ruilin) 添加“星期几”标识
        for i in range(7):
            self.month_lendar_layout.addWidget(self.weekday_widgets[i], 1, i, 1, 1)
            weekday_label = QLabel('\n\n\n\n\n        星期' + str(i + 1), self.weekday_widgets[i])
        
        # $(ruilin) 为每一天添加一个对应的按钮，其上面的文字显示任务信息
        for i in range(6):
            for j in range(7):
                self.month_lendar_layout.addWidget(self.widgets[7 * i + j], i + 2, j, 1, 1)
                

        self.flush()

    def year__month_changed(self):

        # (ruilin) 断开之前的信号与槽的链接
        # (ruilin) 如果没有下面这几行代码，会导致一个信号链接到多个槽里(多重链接到一个函数)，最后槽函数被多次调用        
        first_day_of_month = datetime.datetime(
            year = self.current_year,
            month = self.current_month,
            day = 1
        )
        cur_day = first_day_of_month.weekday()
        this_month_days = calendar.Calendar().itermonthdates(self.current_year, self.current_month)
        for day in this_month_days:
            if day.month != self.current_month: continue
            self.widgets[cur_day].clicked.disconnect(self.trigger_display_today)
            cur_day += 1
        # (ruilin) /**/

        self.current_year = int(self.year_spinbox.value())
        self.current_month = int(self.month_spinbox.value())
        self.flush()


    # $(ruilin) 将按钮及其对应的信息刷新
    def flush(self):
        
        # $(ruilin) 确定某个月的第一天是星期几
        first_day_of_month = datetime.datetime(
            year = self.current_year,
            month = self.current_month,
            day = 1
        )

        # $(ruilin) cur_day 将对应一个个按钮
        cur_day = first_day_of_month.weekday()

        print('current = ', self.current_year, self.current_month)
        this_month_days = calendar.Calendar().itermonthdates(self.current_year, self.current_month)

        for wg in self.widgets: # $(ruilin) 刷新之前清空
            wg.setText('')

        # (ruilin) 这个字典映射关系为 { idx of self.widgets => date}
        # (ruilin) 其作用是在点击按钮的时候能够方便的找到是哪一天

        self.idx_to_day = {}
        for day in this_month_days:
            # print('day = ', day, ' cur_day = ', cur_day)
            if day.month != self.current_month: continue

            today_ddl_count = 0
            today_tasks = []

            for tsk in self.schedule.tasks:

                if tsk.tasktype == Task_type.NORMAL:
                    (yy1, mm1, dd1) = tsk.ddl_year_and_month()
                    if yy1 == day.year and mm1 == day.month and dd1 == day.day:
                        today_ddl_count += 1
                        today_tasks.append(tsk)
                else:
                    (yy1, mm1, dd1) = tsk.start_year_and_month()
                    (yy2, mm2, dd2) = tsk.ddl_year_and_month()
                    t1 = datetime.datetime(yy1, mm1, dd1)
                    t2 = datetime.datetime(yy2, mm2, dd2)
                    t0 = datetime.datetime(day.year, day.month, day.day)
                    if tsk.check_someday_if_finished(t0.date()): continue
                    if t1 <= t0 <= t2:
                        today_ddl_count += 1
                        today_tasks.append(tsk)

            today_text = str(day)
            if today_ddl_count:
                today_text += '\n 今日有{}件事情'.format(today_ddl_count)

                # (ruilin) 在当前日期上显示三条事情
                for i in range(min(3, len(today_tasks))):
                    tsk = today_tasks[i]
                    today_text += "\n{} : {}".format(i + 1, tsk.title)

            # (ruilin) 在按钮上面展示相应的文字
            self.widgets[cur_day].setText(today_text)

            # (ruilin) 点击按钮可以查看详细的信息
            self.widgets[cur_day].clicked.connect(self.trigger_display_today)

            # (ruilin) 设置映射字典
            self.idx_to_day[cur_day] = day

            cur_day += 1

    def trigger_do_nothing(self):
        # (ruilin) 什么也不做
        pass

    def trigger_display_today(self):

        # (ruilin) idx 是这个按钮的 id
        idx = self.widgets.index(self.sender())
        print('id = ', idx, self.idx_to_day[idx])

        # (ruilin) 对 self.today 的解释：每当点击月历模式中的一个大按钮，self.today 便会切换到这一天
        self.today = self.idx_to_day[idx]

        # (ruilin) 弹出详细信息窗口，进行基本设置
        self.info_dialog = QDialog()
        self.info_dialog.setWindowTitle('任务详情')
        self.info_dialog.resize(1000, 800)

        self.info_dialog_layout = QGridLayout()
        self.info_dialog.setLayout(self.info_dialog_layout)

        # (ruilin) 弹出详细信息窗口中显示主题为一个canvas
        self.canvas = QWidget()
        self.canvas_layout = QVBoxLayout()
        self.canvas.setLayout(self.canvas_layout)
        
        # (ruilin) 使用ScrollArea 来包装这个Canvas
        self.canvas_scroll_area = QScrollArea()
        self.canvas_scroll_area.setWidget(self.canvas)
        self.canvas_scroll_area.setWidgetResizable(True)
        self.info_dialog_layout.addWidget(self.canvas_scroll_area)

        # (ruilin) 将是当日的任务展示出来
        goint_to_show_task = []
        for tsk in self.schedule.tasks:

            if tsk.tasktype == Task_type.NORMAL:
                (yy1, mm1, dd1) = tsk.ddl_year_and_month()
                if yy1 == self.today.year and mm1 == self.today.month and dd1 == self.today.day:
                    goint_to_show_task.append(tsk)
                    temp_bridge_widget = TaskSmallWidget_2(tsk)
                    self.canvas_layout.addWidget(temp_bridge_widget)
                    temp_bridge_widget.del_but.clicked.connect(self.trigger_bridge_widget_del)
            else:
                (yy1, mm1, dd1) = tsk.start_year_and_month()
                (yy2, mm2, dd2) = tsk.ddl_year_and_month()
                t1 = datetime.datetime(yy1, mm1, dd1)
                t2 = datetime.datetime(yy2, mm2, dd2)
                t0 = datetime.datetime(self.today.year, self.today.month, self.today.day)
                if tsk.check_someday_if_finished(t0.date()): continue
                if t1 <= t0 <= t2:
                    goint_to_show_task.append(tsk)
                    temp_bridge_widget = TaskSmallWidget_2(tsk)
                    self.canvas_layout.addWidget(temp_bridge_widget)
                    temp_bridge_widget.del_but.clicked.connect(self.trigger_bridge_widget_del)



        self.info_dialog.exec_()

    # (ruilin) 不知道为啥，需要用这个函数来请理 Layout
    def clear_layout(self, layout):
        item_list = list(range(layout.count()))
        item_list.reverse()
        for i in item_list:
            item = layout.itemAt(i)
            layout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()

    # (ruilin) 在详情展示中选择删除该任务
    def trigger_bridge_widget_del(self):
        print(self.sender())
        print(self.sender().parent())
        print(self.sender().parent().parent())
        print('self.today = ', self.today, type(self.today))

        bridge_widget = self.sender().parent()
        canvas = self.sender().parent().parent()

        if bridge_widget.task.tasktype == Task_type.DAILY:
            bridge_widget.task.set_someday_finished(self.today)
        else:   # (ruilin) 普通任务是直接删掉
            self.schedule.remove_designated_task(bridge_widget.task)
        
        
        self.flush()
        
        self.clear_layout(self.canvas_layout)
        # (ruilin) 一个暴力的刷新方式
        for tsk in self.schedule.tasks:

            if tsk.tasktype == Task_type.NORMAL:
                (yy1, mm1, dd1) = tsk.ddl_year_and_month()
                if yy1 == self.today.year and mm1 == self.today.month and dd1 == self.today.day:
                    temp_bridge_widget = TaskSmallWidget_2(tsk)
                    self.canvas_layout.addWidget(temp_bridge_widget)
                    temp_bridge_widget.del_but.clicked.connect(self.trigger_bridge_widget_del)
            else:
                (yy1, mm1, dd1) = tsk.start_year_and_month()
                (yy2, mm2, dd2) = tsk.ddl_year_and_month()
                t1 = datetime.datetime(yy1, mm1, dd1)
                t2 = datetime.datetime(yy2, mm2, dd2)
                t0 = datetime.datetime(self.today.year, self.today.month, self.today.day)

                if tsk.check_someday_if_finished(t0.date()): continue
                if t1 <= t0 <= t2:
                    temp_bridge_widget = TaskSmallWidget_2(tsk)
                    self.canvas_layout.addWidget(temp_bridge_widget)
                    temp_bridge_widget.del_but.clicked.connect(self.trigger_bridge_widget_del)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Monthlendar()
    ui.show()
    sys.exit(app.exec_())




