from .CoreTask import *
from .CoreEnum import *


def cmp_by_ddl(x: Task, y: Task):
    x_ddl_time = time.mktime(time.strptime(x.ddl, "%Y-%m-%d %H:%M"))
    y_ddl_time = time.mktime(time.strptime(y.ddl, "%Y-%m-%d %H:%M"))
    return -1 if x_ddl_time < y_ddl_time else 1


def cmp_by_importance(x: Task, y: Task):
    x_importance = get_importance_value(x.importance_level)
    y_importance = get_importance_value(y.importance_level)
    return -1 if x_importance > y_importance else 1


def cmp_by_title(x: Task, y: Task):
    return -1 if x.title < y.title else 1


def cmp_by_tag(x: Task, y: Task):
    return -1 if x.tag < y.tag else 1


def cmp_by_status(x: Task, y: Task):
    return -1 if get_status_value(x.status) > get_status_value(y.status) \
       else 1
