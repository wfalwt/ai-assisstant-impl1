import json
import os

import api
from agent.db import get_app_db_conn
from agent.db.query_result import get_table_ddl, get_schema_prompt
from agent.test.mf_schema import AppData
from api.model.task.app_schema import BusinessSystem
from api.model.task.translation import Translation
from api.model.tool.mf_schema import Object

tables = os.environ.get("CHART_SOURCE")
table_schema_from = os.environ.get("CHART_SOURCE_FROM", "ddl")


def get_app_prompt() -> ():
    tables_desc = get_table_desc()
    return (f""" AI助手，可以通过调用工具来处理用户的请求。以下数据表的结构，你可能会用到：
            {tables_desc}
            请将工具返回的内容直接返回给用户，你总是用中文回复用户。""")


def get_ide_prompt() -> ():
    return ("""
    你是 AI助手，可以通过调用工具来处理用户的请求。
    在您你准备调用工具之前，请先与用户进行互动，确认以下数据是否正确：

    1. 调用的工具名称
    2. 调用工具的参数列表
   
    请询问用户是否确认使用这些数据，并在用户确认后继续。如果没有得到用户的确认，请提示用户提供正确的数据或进行必要的修改。
    在使用工具前，要跟用户确认调用工具的数据，用户确认后，才能调用工具。
    """)


def get_rag_prompt() -> ():
    return (f""" AI助手，你可以通过文档检索回答用户的问题，
    你总是会以markdown的方式回复用户。""")


def get_task_prompt(task) -> ():
    match task:
        case 'translation':
            return ("你是一个语言专家，擅长将各种语言进行翻译。")
        case 'it_moe':
            return (f"""
    你是一位资深的IT专家，擅长将业务需求转化为构建IT系统的需求，进而构建基础的业务系统。
    用户提出有关系统的需求后，你要：
    - 提取出有关业务对象以及对象包含的字段
    - 梳理出业务相关流程转化为处理对象的相关函数
    结果按照schema的json格式输出。
    schema:
    {json.dumps(AppData.model_json_schema(), ensure_ascii=False, indent=2)}
    """)
        case 'mf_exp':
            return (f"""
    你是一位经验的丰富的专家，能根据客户的输入的内容提取关键信息。你可以：
    - 根据用户提出的业务对象，给出业务对象包含的字段信息，给出的数据格式按照以下的json的schema格式输出：
    {json.dumps(Object.model_json_schema(), ensure_ascii=False, indent=2)}
    """)


def get_table_desc() -> str:
    return """
    xxx日报表 table_xx，包含字段如下:
        - f_1:	字段1
    """
    app_version_id = api.app.state.app_version_id
    table_description = ""
    if table_schema_from == "ddl":
        db_conn = get_app_db_conn(app_version_id)
        if tables:
            table_array = tables.split(",")
            for table_name in table_array:
                table_description += get_table_ddl(table_name, db_conn) + "\n"
    elif table_schema_from == "meta":
        db_conn = get_app_db_conn(app_version_id, "meta")
        if tables:
            table_array = tables.split(",")
            table_description = get_schema_prompt(db_conn, table_array)
    return table_description


def get_doc_list(doc_root: str) -> list[str]:
    doc_list = []
    paths = os.walk(doc_root)
    for path, _, file_lst in paths:
        for file_name in file_lst:
            doc_list.append(os.path.join(path, file_name))
    return doc_list
