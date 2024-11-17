from typing import Union
from pydantic import BaseModel, Field


class Translation(BaseModel):
    """
    将内容翻译为指定的语言，要求将content字段的内容翻译为dest_lang的语言，只翻译content中value的内容，key保持不变
    """
    src_lang: Union[str] = Field(default=None, description="内容对应的语言，默认为中文", examples=["中文"])
    dest_lang: str = Field(title="要翻译的语言", description="要翻译的语言", examples=["英文"])
    content: dict = Field(title="要翻译的内容", description="要翻译的内容，只要求翻译value的内容，key保持不变",
                          examples=[{"key": "需要翻译的内容"}])


if __name__ == "__main__":
    import json
    print(json.dumps(Translation.model_json_schema(), ensure_ascii=False, indent=2))
