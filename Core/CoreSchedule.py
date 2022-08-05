from .CoreTask import Task, load_task_from_dict
from .CoreEnum import *
from .CoreArgorithm import *
import functools


class Schedule:
    def __init__(self):
        self.tasks = list()

    def change_tasks(self, task_list):
        self.tasks = task_list

    def add_task(self, task: Task):
        self.tasks.append(task)

    def remove_designated_task(self, task: Task):
        self.tasks.remove(task)

    def remove_task(self):      # 删除状态被设定为 DELETED 的task
        new_tasks = list()
        for _ in self.tasks:
            if _.status != TaskStatus.DELETED:
                new_tasks.append(_)
        self.tasks = new_tasks

    def to_dict(self):
        return [task.to_dict() for task in self.tasks]

    # =============================================================
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


def load_schedule_from_list(l : list) -> Schedule:
    s = Schedule()
    s.change_tasks([load_task_from_dict(dic) for dic in l])
    return s