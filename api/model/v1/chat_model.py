from enum import Enum
from typing import Union

from pydantic import BaseModel, Field


class ChatType(Enum):
    chat_agent_ide = "ide_agent"
    chat_agent_app = "app_agent"
    chat_rag = "rag"


class ChatInput(BaseModel):
    app_id: Union[str] = Field(description="应用ID", default=None, examples=["88fc43c387ba9c5d"])
    app_version_id: Union[str] = Field(description="应用对应的版本ID", default=None,
                                       examples=["66c3ffa2dbc9122e758da28d"])
    login_id: Union[str] = Field(description="登录标识，创建对象页面等操作需要传此参数", default=None,
                                 examples=["A9259707947DCCABBAA3ABDE672170FD"])
    message: str = Field(description="交互内容", examples=[
        "生成一个根据物料编号和物料名称查询物料基础表中物料规格、物料单位、物料状态的查询函数"])
    chat_type: str = Field(
        description=" 聊天的类型: rag 表示知识库问答， ide_agent 表示使用与建模平台集成的工具， app_agent 表示与应用平台的集成的工具 ",
        default="rag", examples=["rag"], json_schema_extra={'enum': ["rag", "ide_agent", "app_agent"]})


class ChatHistory(BaseModel):
    role: str = Field(description="角色，其中assistant 代表AI，user代表用户")
    content: str = Field(description="内容，如果role为assistant 代表是AI返回的内容，如果为user代表是用户的内容")


class ChatHistoryOutput(BaseModel):
    response: list[ChatHistory] = Field(description="聊天记录")


class ChatOutput(BaseModel):
    response: str = Field(description="AI 返回的生成内容")


if __name__ == "__main__":
    print(ChatHistory.model_json_schema())