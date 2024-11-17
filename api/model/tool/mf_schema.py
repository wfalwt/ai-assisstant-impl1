from enum import IntEnum
from typing import Any

from pydantic import BaseModel, Field


class ObjectFieldType(IntEnum):
    """对象字段的类型，如下：
    1. 文本
    2. 多行文本
    3. 数字
    4. 日期
    5. 日期时间
    6. 单选
    7. 多选
    8. 下拉框
    9. 附件
    10. 图片
    11. 流水号
    12. 变量
    13. 时间
    14. 部门
    15. 员工
    16. 岗位
    17. 年周
    """

    text = 1
    textarea = 2
    numbers = 3
    date = 4
    datetime = 5
    radio = 6
    checkbox = 7
    select = 8
    attachment = 9
    image = 10
    seqno = 11
    variable = 12
    time = 13
    department = 14
    employer = 15
    position = 16
    week = 17


class ObjectField(BaseModel):
    """对象的字段属性"""

    field_name: str = Field(description="对象的字段名称，必须使用中文", max_length=50, examples=["家庭地址"])
    field_alias: str = Field(
        description="对象的字段别名，必须使用英文，可以根据字段名称翻译为英文单词，使用小写，多个单词用_连接，限制在50个字符以内",
        max_length=50, examples=["home_address"])
    field_type: ObjectFieldType = Field(description="""对象的字段类型，请选择枚举类型中的一种，数字代表的类型如下：
                            1. 文本
                            2. 多行文本
                            3. 数字
                            4. 日期
                            5. 日期时间
                            6. 单选
                            7. 多选
                            8. 下拉框
                            9. 附件
                            10. 图
                            11. 流水号
                            12. 变量
                            13. 时间
                            14. 部门
                            15. 员工
                            16. 岗位
                            17. 年周
                        """)
    field_default_value: Any = Field(description="字段默认值", default=None)
    field_description: str = Field(description="对象的字段描述信息")
    field_enumerate: list[str] = Field(description="对象的枚举值，当字段的类型为单选，多选，下拉框时需要设定",
                                       default=None)
    field_precision: int = Field(description="对象的字段精度，如果字段为数值类型时设定", default=0)
    field_max_length: int = Field(description="对象的字段最大长度，当字段为文本内容时设定", default=50)
    field_max_value: int = Field(description="对象的字段最大值，当字段为数值时设定", default=999999999)


class Object(BaseModel):
    """创建一个业务对象，业务对象相对于数据表⽤于定义数据字段和关联"""

    object_name: str = Field(description="需要创建对象的名称，必须使用中文", max_length=50, examples=["学生基础信息"])
    object_alias: str = Field(
        description="需要创建对象的别名，必须使用英文，可以根据对象名称翻译为对应的英文，使用小写，多个单词用_连接",
        max_length=50, examples=["student_info"])
    object_description: str = Field(description="对象的描述信息", default=None)
    object_fields: list[ObjectField] = Field(description="对象包含的字段列表")


class FaasFieldKind(IntEnum):
    kind_alias = 1
    kind_name = 2


class FaasField(BaseModel):
    field_name: str = Field(description="对象的字段名称", examples=["姓名"])
    field_type: FaasFieldKind = Field(
        description="字段的类型，如果字段为中文则是字段名称，如果为英文则是字段别名， 1. 字段别名，2.字段名称",
        examples=[2])


class FaasType(IntEnum):
    write_opera = 1
    read_opera = 2


class FaasActionType(IntEnum):
    create = 1
    update = 2
    delete = 3
    advance_update = 4


class FaasConditionType(IntEnum):
    rel_normal = 0
    rel_and = 1
    rel_or = 2


class FaasObject(BaseModel):
    """创建一个函数，函数用于处理数据的新增、存储、删除、查询、修改等基本操作"""

    faas_name: str = Field(description="需要创建函数的名称,必须要使用中文", max_length=100,
                           examples=["查询学生基本信息"])
    faas_alias: str = Field(
        description="需要创建函数的别名，请输入英文，可以根据输入的函数名称自动转成英文，使用小写，多个单词用_连接",
        max_length=200, examples=["search_student_info"])
    faas_type: FaasType = Field(
        description="需要创建函数的类型： 1. 动作函数，如更新，新增等操作 2. 查询函数，如查询数据等读取操作", examples=[2])
    assoc_object: str = Field(description="需要关联的业务对象，可以输入对象名或者对象别名", examples=["学生信息"])
    action_type: FaasActionType = Field(description="对象的操作类型 : 1. 创建 2. 更新 3. 删除 4. 高级更新",
                                        examples=[1])
    faas_assign_fields: list[FaasField] = Field(description="函数需要操作的字段，如更新的字段或者查询的字段", default=[],
                                                examples=[[]])
    faas_condition_fields: list[FaasField] = Field(description="函数查询条件需要的字段", default=[],
                                                   examples=[{"field_name": "姓名", "field_type": 2}])
    faas_condition_type: FaasConditionType = Field(
        description="函数查询字段间的关联关系，如并且、或者，其中 0. 无关系 1. 并且 2. 或者", default=None, examples=[1])
