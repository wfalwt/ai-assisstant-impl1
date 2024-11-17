from pydantic import BaseModel, Field


class TableField(BaseModel):
    field_name: str = Field(title="字段名", description="字段名称，小写英文，多个单词用下划线连接", max_length=30)
    field_desc: str = Field(title="字段描述", description="字段描述，中文简单描述字段的作用", max_length=30)
    field_type: str = Field(title="字段类型", description="字段类型，使用sql语句中的类型表示")


class Table(BaseModel):
    table_name: str = Field(title="表名", description="表名，使用小写英文，多个单词用下划线连接", max_length=30)
    table_desc: str = Field(title="表的描述", description="描述信息，用中文简单描述表的功能", max_length=30)
    table_fields: list[TableField] = Field(title="字段列表", description="表中包含的字段")


class BusinessWorkflow(BaseModel):
    workflow_name: str = Field(title="流程名称", description="流程名称，使用小写英文，多个单词用下划线连接",
                               max_length=30)
    workflow_desc: str = Field(title="流程描述", description="描述信息，用中文简单描述流程", max_length=255)
    workflow_dsl: str = Field(title="流程DSL", description="流程的DSL描述，用JSON结构的DSL描述流程业务逻辑",
                              max_length=1000)


class BusinessSystem(BaseModel):
    table_list: list[Table] = Field(description="数据表列表")
    workflow_list: list[BusinessWorkflow] = Field(description="流程列表")


if __name__ == "__main__":
    import json
    print(json.dumps(BusinessSystem.model_json_schema(), ensure_ascii=False, indent=2))
