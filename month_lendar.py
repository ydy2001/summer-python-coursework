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
)
from matplotlib import widgets

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
        self.current_year = today.year
        self.current_month = today.month

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

        for day in this_month_days:
            # print('day = ', day, ' cur_day = ', cur_day)
            if day.month != self.current_month: continue

            today_ddl_count = 0
            today_tasks = []

            for tsk in self.schedule.tasks:
                (yy1, mm1, dd1) = tsk.ddl_year_and_month()
                if yy1 == day.year and mm1 == day.month and dd1 == day.day:
                    today_ddl_count += 1
                    today_tasks.append(tsk)

            today_text = str(day)
            if today_ddl_count:
                today_text += '\n 今日有{}件事情截止'.format(today_ddl_count)

                for i in range(min(3, len(today_tasks))):
                    tsk = today_tasks[i]
                    today_text += "\n{} : {}".format(i + 1, tsk.title)

            self.widgets[cur_day].setText(today_text)
            cur_day += 1

            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Monthlendar()
    ui.show()
    sys.exit(app.exec_())




