# ===============================================================
# (blame) ruilin
# 月历模式，把 calender 作为一个 Widget 来实现
# ===============================================================

import sys
from calendar import calendar

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

from Core.CoreSchedule import Schedule

# Monthlendar 是我自己创的一个词，指月历
class Monthlendar(QWidget):

    def __init__(self, schedule : Schedule = None):
        super().__init__()
        self.schedule = schedule    # schedule = [task for task in 用户的所有任务]
        self.resize(2000, 1500)
        month_lendar_layout = QGridLayout() # 网格内部通过网格布局来实现
        self.setLayout(month_lendar_layout)

        # $(ruilin) 选择年份
        year_spinbox = QSpinBox()
        year_spinbox.setRange(2000, 2100)
        year_spinbox.setSingleStep(1)
        month_lendar_layout.addWidget(year_spinbox, 0, 1, 1, 1)

        # $(ruilin) 选择月份
        month_spinbox = QSpinBox()
        month_spinbox.setRange(1, 12)
        month_spinbox.setSingleStep(1)
        month_lendar_layout.addWidget(month_spinbox, 0, 3, 1, 1)


        widgets = [QPushButton() for i in range(5 * 7)]     # 创建 5行7列的小部件
        weekday_widgets = [QWidget() for i in range(7)]     # 7列的小部件，用于显示星期几表示    

        self.button_Adaptive = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        for wg in widgets:
            wg.setSizePolicy(self.button_Adaptive)

        # $(ruilin) 添加“星期几”标识
        for i in range(7):
            month_lendar_layout.addWidget(weekday_widgets[i], 1, i, 1, 1)
            weekday_label = QLabel('\n\n\n      星期' + str(i + 1), weekday_widgets[i])
        
        # $(ruilin) 为每一天添加一个对应的按钮，其上面的文字显示任务信息
        for i in range(5):
            for j in range(7):
                month_lendar_layout.addWidget(widgets[7 * i + j], i + 2, j, 1, 1)
                

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Monthlendar()
    ui.show()
    sys.exit(app.exec_())




