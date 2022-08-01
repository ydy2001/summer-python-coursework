import time
from CoreEnum import *


class Task:
    def __init__(self, ddl, title='unnamed', content='', remark='',
                 start_time=time.strftime("%Y-%m-%d %H:%M", time.localtime()),
                 importance_level=ImportanceLevel.NORMAL, tag='uncategorized'):
        self.ddl = ddl                            # ddl，要求格式为 YYYY-MM-DD hh:mm
        self.title = title                        # 标题
        self.content = content                    # 具体内容
        self.remark = remark                      # 备注
        self.start_time = start_time              # 任务开始时间， 默认为当前系统时间，要求格式为 YYYY-MM-DD hh:mm
        self.importance_level = importance_level  # 重要程度
        self.tag = tag                            # 任务tag
        self.status = TaskStatus.NOT_STARTED
        self.update_status()                      # 根据当前时间，start_time，ddl更新任务状态

    def update_status(self):                      # 根据当前时间和状态更新任务状态
        #########################################################
        if self.status == TaskStatus.DELETED \
        or self.status == TaskStatus.EXPIRED \
        or self.status == TaskStatus.DONE:
            return # 对于已完成、被删除和过期未完成的任务，不适用此方法
        #########################################################
        now_time = time.time() # 当前时间戳
        ddl_time = time.mktime(time.strptime(self.ddl, "%Y-%m-%d %H:%M")) # ddl时间戳
        start_time = time.mktime(time.strptime(self.start_time, "%Y-%m-%d %H:%M")) # start_time时间戳
        if now_time < start_time:
            self.status = TaskStatus.NOT_STARTED
        elif start_time <= now_time < ddl_time:
            self.status = TaskStatus.IN_PROCESS
        else:
            self.status = TaskStatus.EXPIRED

    def change_status(self, status):              # 主动指定更新任务状态
        self.status = status

    def change_tag(self, tag_str):
        self.tag = tag_str

    def change_ddl(self, new_ddl):
        self.ddl = new_ddl

    def change_content(self, content_str, append=False):
        if append:
            self.content += content_str
        else:
            self.content = content_str

    def change_remark(self, remark_str, append=False):
        if append:
            self.remark += remark_str
        else:
            self.remark = remark_str

    def change_importance_level(self, new_importance_level):
        self.importance_level = new_importance_level

    def increase_importance_level(self, increment=1):
        if self.importance_level == ImportanceLevel.URGENT:
            return
        value = get_importance_value(self.importance_level)
        if value + increment > 4:
            self.importance_level = ImportanceLevel.URGENT
        else:
            self.importance_level = ImportanceLevel(value + increment)

    def decrease_importance_value(self, decrement=1):
        if self.importance_level == ImportanceLevel.INSIGNIFICANT:
            return
        value = get_importance_value(self.importance_level)
        if value - decrement < 0:
            self.importance_level = ImportanceLevel.INSIGNIFICANT
        else:
            self.importance_level = ImportanceLevel(value - decrement)
