import json
import time
from typing import Union

import json5
import pymysql
from qwen_agent.tools.base import register_tool, BaseTool
from agent.db import get_app_db_conn
import api
from agent.db.parse import extract_table_names
from agent.db.query_result import get_schema_by_meta
from agent.util.json_util import SpecialDataEncoder
from mindforce.app.chart_support import put_chart_file_content
from agent.chart.data_type import is_date, is_number, is_text


def _parse_field_type(key, value) -> int:
    """
    parse field type to table field type
    1.文本 2.多行文本 3.数字 4.日期 5.日期时间 6.单选 7.多选 8.下拉框 9.附件 10.图片 11.流水号 12.变量 13.时间
    """
    if is_date(key, value):
        return 5
    elif is_number(value):
        return 3
    elif is_text(value):
        return 1

    return 1


@register_tool("table_query")
class TableQuery(BaseTool):
    name = "table_query"
    description = '查询统计数据，以表格的方式展示数据，根据输入的SQL返回查询的数据'
    parameters = [{
        'name': 'sql',
        'type': 'string',
        'description': '要查询的SQL',
        'required': True
    }]

    def call(self, params: Union[str, dict], **kwargs) -> Union[str, list, dict]:
        sql = json5.loads(params)['sql']
        tables = extract_table_names(sql)
        app_version_id = api.app.state.app_version_id
        meta_db_conn = get_app_db_conn(app_version_id, "meta")
        fields_mapping = dict()
        for table in tables:
            schema_dict = get_schema_by_meta(table, meta_db_conn, False)
            for fields_info in schema_dict.values():
                for field in fields_info.get("fields"):
                    field_alias = field.get("alias")
                    fields_mapping[field_alias] = field
        db_conn = get_app_db_conn(app_version_id)
        cursor = db_conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        result = cursor.fetchall()
        # return json.dumps(result, cls=SpecialDataEncoder, ensure_ascii=False)
        if len(result) == 0:
            return "没有找到对应的数据"

        data_sample = result[0]
        table_fields = data_sample.keys()
        column_list = []
        search_list = []
        print(fields_mapping)
        for field in table_fields:
            column = {
                "name": fields_mapping[field].get("name") if fields_mapping.get(field) else field,
                "alias": field,
                "type": fields_mapping[field].get("type") if fields_mapping.get(field) else
                _parse_field_type(data_sample[field], field)
            }
            column_list.append(column)
            if column["type"] == 1 or column["type"] == 5:
                search_list.append(field)

        table_data = {
            "type": "table",
            "columnList": column_list,
            "searchList": search_list,
            "data": result
        }

        data_json = json.dumps(table_data, cls=SpecialDataEncoder, ensure_ascii=False)
        table_js_content = f"var data={data_json};"
        table_js_file_name = "table-" + time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + ".js"
        table_url = put_chart_file_content(table_js_file_name, table_js_content)
        return table_url
