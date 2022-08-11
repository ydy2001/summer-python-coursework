from enum import Enum, unique
from turtle import done


@unique
class Task_type(Enum):
    NORMAL = 0
    DAILY = 1

@unique
class UI_mode(Enum):
    TRADITIONAL = 0
    CALANDAR = 1


@unique
class TaskStatus(Enum):
    DELETED = 0       # 被删除
    EXPIRED = 1        # 过期未完成
    DONE = 2           # 顺利完成
    NOT_STARTED = 3     # 未开始
    IN_PROCESS = 4      # 进行中

TaskStatus_to_int = {
    TaskStatus.DELETED : 0,   
    TaskStatus.EXPIRED : 1,       
    TaskStatus.DONE : 2,       
    TaskStatus.NOT_STARTED : 3,     
    TaskStatus.IN_PROCESS : 4,      
}

TaskStatus_to_str = {
    TaskStatus.DELETED : '已删除',   
    TaskStatus.EXPIRED : '已超时',       
    TaskStatus.DONE : '已完成',       
    TaskStatus.NOT_STARTED : '尚未开始',     
    TaskStatus.IN_PROCESS : '进行中',      
}


Int_to_TaskStatus = { value : key for (key, value) in TaskStatus_to_int.items()}

@unique
class ImportanceLevel(Enum):
    INSIGNIFICANT = 0
    NORMAL = 1
    NOTE_WORTHY = 2
    IMPORTANT = 3
    URGENT = 4

Importance_to_int = {
    ImportanceLevel.INSIGNIFICANT : 0,
    ImportanceLevel.NORMAL : 1,
    ImportanceLevel.NOTE_WORTHY : 2,
    ImportanceLevel.IMPORTANT : 3,
    ImportanceLevel.URGENT : 4
}

Int_to_importance = { value : key for (key, value) in Importance_to_int.items()}




def get_importance_value(other):
    if other == ImportanceLevel.INSIGNIFICANT:
        return 0
    elif other == ImportanceLevel.NORMAL:
        return 1
    elif other == ImportanceLevel.NOTE_WORTHY:
        return 2
    elif other == ImportanceLevel.IMPORTANT:
        return 3
    else:
        return 4


def get_status_value(other):
    if other == TaskStatus.DELETED:
        return 0
    elif other == TaskStatus.EXPIRED:
        return 1
    elif other == TaskStatus.DONE:
        return 2
    elif other == TaskStatus.NOT_STARTED:
        return 3
    else:
        assert False
