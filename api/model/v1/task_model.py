from typing import Union

from pydantic import BaseModel, Field


class TaskInput(BaseModel):
    task_name: str = Field(
        description="任务名称，现有任务包括 translation 翻译任务， it_moe 信息系统专家任务， mf_exp MindForce 专家任务",
        default="translation", json_schema_extra={'enum': ["translation", "it_moe", "mf_exp"]})
    content: str = Field(
        description="任务内容，提交给任务的数据，可以是结构化的数据也可以是自然语言，取决于具体任务的要求")
    events_args: Union[dict] = Field(description="任务后续处理附加参数，由具体任务后续的event决定", default=None)

