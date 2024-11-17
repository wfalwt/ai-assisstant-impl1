from enum import Enum

from pydantic import BaseModel, Field


class ChartType(Enum):
    """
  图表的类型，请选择枚举中的一种，其中:
    line代表折线图，
    interval代表柱状图，
    pie 代表饼图，
    funnel 代表漏斗图，
    symmetricalFunnel 代表对称漏斗图
    """
    chart_line = "line"
    chart_interval = "interval"
    chart_pie = "pie"
    chart_funnel = "funnel"
    chart_symmetrical_funnel = "symmetricalFunnel"


class ChartQuery(BaseModel):
    chart_type: ChartType = Field(description="""图表的类型，请选择枚举中的一种，其中:
                   line代表折线图，
                   interval代表柱状图，
                   pie 代表饼图，
                   funnel 代表漏斗图，
                   symmetricalFunnel 代表对称漏斗图""")
    chart_title: str = Field(description="显示图标的标题", max_length=100)
    sql: str = Field(description="要查询的SQL")
