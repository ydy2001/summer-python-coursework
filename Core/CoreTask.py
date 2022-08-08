import time
from .CoreEnum import (
    Int_to_TaskStatus,
    Int_to_importance,
    TaskStatus_to_int,
    Importance_to_int, 
    ImportanceLevel, 
    TaskStatus, 
    get_importance_value,
)


class Task:
    def __init__(self, 
                 ddl:str, 
                 title:str, 
                 content:str,
                 remark:str,
                 start_time:str,
                 importance_level:ImportanceLevel,
                 tag:str = 'uncategorized',
                 status = TaskStatus.NOT_STARTED
                 ):
        self.ddl = ddl                            # ddl，要求格式为 YYYY-MM-DD hh:mm
        self.title = title                        # 标题
        self.content = content                    # 具体内容
        self.remark = remark                      # 备注
        self.start_time = start_time              # 任务开始时间， 默认为当前系统时间，要求格式为 YYYY-MM-DD hh:mm
        self.importance_level = importance_level  # 重要程度
        self.tag = tag                            # 任务tag
        self.status = status                      # (ruilin) 注意这里通过输入的参数确定，为了载入本地数据
        self.update_status()                      # 根据当前时间，start_time，ddl更新任务状态

    def update_status(self):                      # 根据当前时间和状态更新任务状态
        # 对于已完成、被删除和过期未完成的任务，不适用此方法
        if self.status in [TaskStatus.DELETED, TaskStatus.EXPIRED, TaskStatus.DONE]:
            return 
        
        now_time = time.time() # 当前时间戳
        ddl_time = time.mktime(time.strptime(self.ddl, "%Y-%m-%d %H:%M")) # ddl时间戳
        start_time = time.mktime(time.strptime(self.start_time, "%Y-%m-%d %H:%M")) # start_time时间戳
        if now_time < start_time:
            self.status = TaskStatus.NOT_STARTED
        elif start_time <= now_time < ddl_time:
            self.status = TaskStatus.IN_PROCESS
        else:
            self.status = TaskStatus.EXPIRED

    def to_string(self) -> str:
        text = self.title + \
               '\n任务标签: ' + self.tag + \
               '\n截止时间: ' + self.ddl
        '''
        if len(self.content) != 0:
            text += '\n内容: ' + self.content
        if len(self.remark) != 0:
            text += '\n备注: ' + self.remark
        '''
        return text

    # 有关文件保存的 ==============================================================
    def to_dict(self) -> dict:
        return {
            'ddl' : str(self.ddl),
            'title' : self.title,
            'content' : self.content,
            'remark' : self.remark,
            'start_time' : str(self.start_time),
            'importance_level' : Importance_to_int[self.importance_level],
            'tag': self.tag,
            'status' : TaskStatus_to_int[self.status]
        }


    def ddl_year_and_month(self) :
        tsk_ddl = time.strptime(self.ddl, "%Y-%m-%d %H:%M")
        return (tsk_ddl.tm_year, tsk_ddl.tm_mon, tsk_ddl.tm_mday)

    # 以下函数暂时还未开始使用
    # Currently not used. ========================================================
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


# $(ruilin) 通过我们的协议，来载入一个用 json 存放的 Task
def load_task_from_dict(dic : dict) -> Task:
    return Task(
        ddl = dic['ddl'],
        title = dic['title'],
        content = dic['content'],
        remark = dic['remark'],
        start_time = dic['start_time'],
        importance_level = Int_to_importance(dic['importance_level']),
        tag = dic['tag'],
        status = Int_to_TaskStatus(dic['status'])
    )


# following code is just for local test
if __name__ == '__main__':
    task = Task('2022-8-1 23:00', start_time='2022-8-1 10:00')
    print(task.status)