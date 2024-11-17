import json
from typing import Union
from qwen_agent.tools import BaseTool
from qwen_agent.tools.base import register_tool

import api
from agent.util.log import log
from api.model.tool.mf_schema import Object
from mindforce.ide.object import create_object, object_fields_add, get_object, get_page_edit_url, get_object_edit_url
from mindforce.ide.page import create_form_page, create_list_page


@register_tool("create_object")
class CreateObject(BaseTool):
    name = "create_object"
    description = '创建一个业务对象，业务对象相对于数据表⽤于定义数据字段和关联。'
    parameters = Object.schema_json()

    def call(self, params: Union[str, dict], **kwargs) -> str:
        params_dict = json.loads(params)
        app_id = api.app.state.app_id
        app_version_id = api.app.state.app_version_id
        login_id = api.app.state.ide_login_id
        object_name = params_dict["object_name"]
        object_alias = params_dict["object_alias"]
        object_description = params_dict["object_description"]
        object_fields = params_dict["object_fields"]
        if not isinstance(object_name, str):
            raise TypeError("object_name必须是字符串")
        if not isinstance(object_alias, str):
            raise TypeError("object_alias必须是字符串")
        if not isinstance(object_fields, list):
            raise TypeError("object_fields必须是列表")
        for field in object_fields:
            if not isinstance(field, dict):
                raise TypeError("object_fields 里面的元素必须是字典")
            if not 'field_alias' in field and not 'field_alias' in field and not 'field_type' in field:
                raise TypeError("object_field 字典里面必须包含field_name，field_alias，field_type")
        try:
            object_id = create_object(app_id, object_name, object_alias, object_description,login_id)
            result = object_fields_add(app_id, object_id, object_fields)
            if result == "success":
                login_id = api.app.state.ide_login_id
                obj_data = get_object(app_id, login_id, object_id)
                object_url = get_object_edit_url(app_id,object_id, object_alias, object_name)
                form_page_id = create_form_page(app_id, app_version_id, obj_data, login_id)
                form_url = get_page_edit_url(app_id, form_page_id, app_version_id, 4)
                list_page_id = create_list_page(app_id, app_version_id, obj_data, login_id, form_page_id)
                list_url = get_page_edit_url(app_id, list_page_id, app_version_id, 3)
                return f"""对象创建成功。相关信息如下：
                        对象名："{object_name}",
                        对象ID："{object_id}",
                        对象编辑页面地址： {object_url}
                        表单页面ID: "{form_page_id}",
                        页面页面ID: "{list_page_id}",
                        表单页面访问地址："{form_url}",
                        列表页面访问地址："{list_url}" 。
                """
            else:
                log.error(f"创建对象{object_name}失败,原因：{result}")
                raise RuntimeError(f"创建对象{object_name}失败,原因：{result}")
        except:
            import traceback
            raise RuntimeError("调用失败:", traceback.format_exc())
