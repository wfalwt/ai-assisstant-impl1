import json
from abc import ABC

from pydantic import BaseModel
from qwen_agent.tools import BaseTool

from api.model.tool.mf_schema import Object


class Task(ABC):
    param_entity: BaseModel
    func_tool: BaseTool

    def call_tool(self):
        tool = self.func_tool
        return tool.call(params=self.param_entity.json())


def task_val(task_name, output_json, event_args):
    match task_name:
        case 'mf_exp':
            for json_entity in output_json:
                try:
                    filtered_entity = _clear_dict(json_entity)
                    print(f"filtered entity {filtered_entity}")
                    object_entity = Object(**filtered_entity)
                    task = Task()
                    task.func_tool = CreateObject()
                    task.param_entity = object_entity
                    return task.call_tool()
                except Exception as e:
                    print(f'Exception : {e}')


def _clear_dict(d):
    if d is None:
        return None
    elif isinstance(d, list):
        return list(filter(lambda x: x is not None, map(_clear_dict, d)))
    elif not isinstance(d, dict):
        return d
    else:
        r = dict(
            filter(lambda x: x[1] is not None,
                   map(lambda x: (x[0], _clear_dict(x[1])),
                       d.items())))
        if not bool(r):
            return None
        return r


def parse_task_content(task_name, content):
    match task_name:
        case 'translation':
            src_lang = content.get("src_lang")
            dest_lang = content.get("dest_lang")
            trans_content = content.get("content")
            return (f"请将以下JSON内容中的所有文本值部分（value）由{src_lang}翻译为{dest_lang}，保持JSON结构不变。请确保翻译后的JSON仍然是有效的JSON"
                    f"格式，并且所有的键和结构都没有变化。请翻译JSON内容:{json.dumps(trans_content, ensure_ascii=False, indent=2)}")

    if isinstance(content, dict):
        return json.dumps(content)
