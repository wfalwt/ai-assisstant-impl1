import json
import time
from abc import ABC
from typing import Union

import json5
import pymysql
from qwen_agent.tools.base import register_tool, BaseTool

import api
from agent.db import get_app_db_conn
from agent.util.log import log
from mindforce.app.chart_support import put_chart_file_content
from agent.chart.chart_base import ChartData, ChartProducer
from agent.util.json_util import SpecialDataEncoder


@register_tool("chart_by_query")
class QueryChart(BaseTool, ABC):
    name = "chart_by_query"
    description = "查询统计数据以图表的方式展示，根据输入的图表类型，查询的sql语句，生成数据的展示图表"
    parameters = [
        {
            "name": "chart_type",
            "description": """
                   图表的类型，请选择枚举中的一种，其中:
                   line代表折线图，
                   interval代表柱状图，
                   pie 代表饼图，
                   funnel 代表漏斗图，
                   symmetricalFunnel 代表对称漏斗图
               """,
            "enum": ["line",
                     "interval",
                     "pie",
                     "funnel",
                     "symmetricalFunnel"],
            "required": True
        },
        {
            'name': 'chart_title',
            'type': 'string',
            'description': '显示图标的标题',
            'required': True
        },
        {
            'name': 'sql',
            'type': 'string',
            'description': '要查询的SQL',
            'required': True
        }
    ]

    def call(self, params: Union[str, dict], **kwargs) -> Union[str, list, dict]:
        params_dict = json5.loads(params)
        app_version_id = api.app.state.app_version_id
        db_conn = get_app_db_conn(app_version_id)
        log.info(f"chart query tool params dict {params_dict}")
        sql = params_dict['sql']
        chart_type = params_dict['chart_type']
        chart_title = params_dict['chart_title']
        cursor = db_conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        result = cursor.fetchall()
        log.info(f"chart query  fetch result {result}")
        chart_data: list[ChartData] = ChartProducer.make_chart_data(chart_type, result)
        chart_data_list: list[dict] = []
        for data in chart_data:
            chart_data_list.append({
                "x": data.x,
                "y": data.y,
                "legend": data.legend
            })
        log.info(f"chart_data_list {chart_data_list}")
        chart_data_query = {
            "type": chart_type,
            "data": chart_data_list,
            "x": "x",
            "y": "y",
            "legend": "legend"
        }
        if chart_title:
            chart_data_query['title'] = chart_title
        data_json = json.dumps(chart_data_query, cls=SpecialDataEncoder, ensure_ascii=False)
        chart_js_content = f"var data={data_json};"
        chart_js_file_name = "chart-" + time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + ".js"
        chart_url = put_chart_file_content(chart_js_file_name, chart_js_content)
        return chart_url
