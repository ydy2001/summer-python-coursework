from CoreEnum import *
from CoreTask import *
from CoreSchedule import *


class User:
    def __init__(self):
        self.schedules = {}

    # 为用户添加一个指定日期的schedule，日期格式要求为 YYYY-MM-DD，默认为当前日期
    def add_date_schedule(self, date=time.strftime("%Y-%m-%d", time.localtime())):
        self.schedules[date] = Schedule()

    # 获取用户指定日期的schedule，日期格式要求为 YYYY-MM-DD，默认为当前日期
    # 若指定日期无schedule，创建空schedule并返回
    def get_date_schedule(self, date=time.strftime("%Y-%m-%d", time.localtime())):
        if date in self.schedules.keys():
            return self.schedules[date]
        else:
            self.schedules[date] = Schedule()
            return self.schedules[date]
