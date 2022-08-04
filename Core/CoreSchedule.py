from .CoreTask import Task
from .CoreEnum import *
from .CoreArgorithm import *
import functools


class Schedule:
    def __init__(self):
        self.tasks = list()

    def add_task(self, task: Task):
        self.tasks.append(task)

    def remove_task(self):      # 删除状态被设定为 DELETED 的task
        new_tasks = list()
        for _ in self.tasks:
            if _.status != TaskStatus.DELETED:
                new_tasks.append(_)
        self.tasks = new_tasks

    def sort_task(self, cmp_func):
        self.tasks.sort(key=functools.cmp_to_key(cmp_func))

    def sort_by_ddl(self):
        self.sort_task(cmp_func=cmp_by_ddl)

    def sort_by_title(self):
        self.sort_task(cmp_func=cmp_by_title)

    def sort_by_tag(self):
        self.sort_task(cmp_func=cmp_by_tag)

    def sort_by_importance(self):
        self.sort_task(cmp_func=cmp_by_importance)

    def sort_by_status(self):
        self.sort_task(cmp_func=cmp_by_status)
