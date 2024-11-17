import json
import re
from datetime import datetime, date
from decimal import Decimal


class SpecialDataEncoder(json.JSONEncoder):
    """
    json序列化的时候处理特殊的数据格式，像decimal，时间日期等,用法：
    json.dumps(result, cls=SpecialDataEncoder, ensure_ascii=False)
    """

    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        return json.JSONEncoder.default(self, obj)


def extract_json(message: str):
    pattern = r"{([^{}]+)}"
    matches = re.findall(pattern, message, re.DOTALL)
    try:
        return [json.loads("{" + match.strip() + "}") for match in matches]
    except Exception:
        raise ValueError(f"Failed to parse: {message}")


def extract_json_from_md(md_content: str):
    json_objects = []
    try:
        json_data = json.loads(md_content)
        json_objects.append(json_data)
        return json_objects
    except json.JSONDecodeError:
        print("directly to decode content to json error , try to parse from md tags")
    pattern = r'```json\n(.*?)\n```'
    matches = re.findall(pattern, md_content, re.DOTALL)
    for match in matches:
        try:
            json_data = json.loads(match.strip())
            json_objects.append(json_data)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON from match: {match}")
    return json_objects
