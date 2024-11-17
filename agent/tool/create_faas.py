import json
from typing import Union
from qwen_agent.tools import BaseTool
from qwen_agent.tools.base import register_tool
from agent.util.log import log
from api import app
from api.model.tool.mf_schema import FaasObject
from mindforce.ide.faas import create_faas, get_faas_edit_url


@register_tool("create_faas")
class CreateFaaS(BaseTool):
    name = "create_faas"
    description = '创建一个函数，函数用于处理数据的新增、存储、删除、查询、修改等基本操作'
    parameters = FaasObject.schema_json()

    def call(self, params: Union[str, dict], **kwargs) -> Union[str, list, dict]:
        params_dict = json.loads(params)
        log.info(f"create_faas param dict :{params_dict}")
        faas_name = params_dict.get("faas_name")
        faas_alias = params_dict.get("faas_alias")
        faas_type = params_dict.get("faas_type")
        assoc_object = params_dict.get("assoc_object")
        faas_assign_fields = params_dict.get("faas_assign_fields")
        faas_condition_fields = params_dict.get("faas_condition_fields")
        action_type = params_dict.get("action_type")
        faas_condition_type = params_dict.get("faas_condition_type")
        app_id = app.state.app_id
        login_id = app.state.ide_login_id
        assign = []
        wheres = []
        if faas_assign_fields:
            for assign_field in faas_assign_fields:
                assign.append({
                    "field": assign_field.get("field_name"),
                    "val_source": assign_field.get("field_type"),
                })
        if faas_condition_fields:
            for condition_field in faas_condition_fields:
                wheres.append({
                    "field": condition_field.get("field_name"),
                    "val_source": condition_field.get("field_type"),
                })
        faas_data = {
            "type": faas_type,
            "title": faas_name,
            "alias": faas_alias,
            "nodes": [
                {
                    "type": 3,
                    "title": f"{faas_name}-数据节点",
                    "action": {
                        "type": action_type,
                        "where_type": faas_condition_type,
                        "object_info": assoc_object,
                        "assign": assign,
                        "where": wheres
                    }
                }
            ]
        }
        print(faas_data)
        try:
            faas_id = create_faas(app_id, login_id, faas_data)
            if faas_id:
                return f"""
                函数ID： {faas_id}
                函数编辑链接： {get_faas_edit_url(app_id,faas_id)}
                """
        except Exception as e:
            return f'函数创建失败:{e.__traceback__}'
