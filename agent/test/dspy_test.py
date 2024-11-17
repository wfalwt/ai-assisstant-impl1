
import os

import dspy
from dotenv import load_dotenv

from agent.test.mf_schema import AppData
from agent.test.translation import Translation

load_dotenv()

model_server = os.environ.get("LLM_OPENAI_API")
model_name = os.environ.get("LLM_MODEL_NAME")
api_key = os.environ.get("LLM_OPENAI_API_KEY")

lm = dspy.OpenAI(model=model_name, api_base=f"{model_server}/", api_key=api_key, max_tokens=24000)
dspy.settings.configure(lm=lm)


class AppDev(dspy.Signature):
    """你是一位资深的IT专家，擅长将业务需求转化为构建IT系统的需求，进而构建基础的业务系统。
    用户提出有关系统的需求后，你要：
    - 提取出有关业务对象以及对象包含的字段
    - 梳理出业务相关流程转化为处理对象的相关函数
    """
    question = dspy.InputField()
    answer: AppData = dspy.OutputField()


class TranslationTask(dspy.Signature):
    question: Translation = dspy.InputField()
    answer: Translation = dspy.OutputField()


print("start to predict by llm")
predict = dspy.TypedChainOfThought(TranslationTask)
pred = predict(
    question=Translation(
        src_lang="中文",
        dest_lang="西班牙语",
        content={
            "zh": {
                "n7szjt2qnk00000000_kix2a2y5b1s0000000": {
                    "value": "",
                    "placeholder": "请输入工单编号"
                },
                "n7szjt2qnk00000000_wo39304z9z40000000": {
                    "value": "",
                    "placeholder": "请输入事项名称"
                },
                "n7szjt2qnk00000000_fasg4cwwaio0000000": {
                    "value": "",
                    "placeholder": "请选择事项级别",
                    "list": [
                        {
                            "value": "1",
                            "label": ""
                        },
                        {
                            "value": "2",
                            "label": ""
                        }
                    ]
                },
                "n7szjt2qnk00000000_yvdfxs9kicw0000000": {
                    "value": "",
                    "placeholder": "请选择当前状态",
                    "list": [
                        {
                            "value": "1",
                            "label": ""
                        },
                        {
                            "value": "2",
                            "label": ""
                        }
                    ]
                }
            },
            "en": {
                "82fmu925zsw00000000_qbearr2ospc0000000": "文本",
                "n7szjt2qnk00000000_kix2a2y5b1s0000000": {
                    "value": "",
                    "prefix": "前缀",
                    "suffix": "后缀",
                    "placeholder": "请输入内容"
                },
                "n7szjt2qnk00000000_wo39304z9z40000000": {
                    "value": "",
                    "prefix": "前缀",
                    "suffix": "后缀",
                    "placeholder": "请输入内容"
                },
                "n7szjt2qnk00000000_fasg4cwwaio0000000": {
                    "value": "",
                    "prefix": "前缀",
                    "suffix": "后缀",
                    "placeholder": "请输入内容",
                    "list": [
                        {
                            "value": "1",
                            "label": "备选1"
                        },
                        {
                            "value": "2",
                            "label": "备选2"
                        }
                    ]
                },
                "n7szjt2qnk00000000_ccumek91nao0000000": "文本",
                "n7szjt2qnk00000000_yvdfxs9kicw0000000": {
                    "value": "",
                    "prefix": "前缀",
                    "suffix": "后缀",
                    "placeholder": "请输入内容",
                    "list": [
                        {
                            "value": "1",
                            "label": "备选1"
                        },
                        {
                            "value": "2",
                            "label": "备选2"
                        }
                    ]
                }
            },
            "type": "zh"
        })
)
print(f"Answer: {pred.answer}")

print(lm.inspect_history(n=1))
