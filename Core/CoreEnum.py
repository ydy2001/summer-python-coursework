from enum import Enum, unique
from turtle import done


@unique
class TaskStatus(Enum):
    DELETED = -3        # 被删除
    EXPIRED = -2        # 过期未完成
    DONE = -1           # 顺利完成
    NOT_STARTED = 0     # 未开始
    IN_PROCESS = 1      # 进行中

TaskStatus_to_int = {
    TaskStatus.DELETED : -3,   
    TaskStatus.EXPIRED : -2,       
    TaskStatus.DONE : -1,       
    TaskStatus.NOT_STARTED : 0,     
    TaskStatus.IN_PROCESS : 1,      
}

Int_to_TaskStatus = { value : key for (value, key) in TaskStatus_to_int.items()}

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

Int_to_importance = { value : key for (value, key) in Importance_to_int.items()}

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
        return -3
    elif other == TaskStatus.EXPIRED:
        return -2
    elif other == TaskStatus.DONE:
        return -1
    elif other == TaskStatus.NOT_STARTED:
        return 0
    else:
        return 1
