import os

from qwen_agent.agents import ReActChat, Assistant

from agent.llm.llm_prompt import get_doc_list, get_rag_prompt, get_task_prompt, get_ide_prompt, get_app_prompt
from agent.tool.chart_by_query import QueryChart

from agent.tool.table_by_query import TableQuery
from agent.util.log import log

model_server = os.environ.get("LLM_OPENAI_API")
model_name = os.environ.get("LLM_MODEL_NAME")
api_key = os.environ.get("LLM_OPENAI_API_KEY")
doc_root = os.environ.get("LLM_RAG_DOC_ROOT")


def get_agent(agent_type="app_agent", **kwargs):
    match agent_type:
        case "app_agent":
            tools = [QueryChart.name, TableQuery.name]
            system_prompt = get_app_prompt()
            llm_cfg = _get_llm_cfg(model_name, model_server, api_key, 0.2)
            log.info(f"app agent system prompt : {system_prompt}")
            print(system_prompt)
            return _get_react_agent(system_prompt, tools, llm_cfg)
        case "rag":
            file_list = get_doc_list(doc_root)
            llm_cfg = _get_llm_cfg(model_name, model_server, api_key, 0.5)
            system_prompt = get_rag_prompt()
            log.info(f"rag system prompt : {system_prompt}")
            return _get_basic_assistant(system_prompt, llm_cfg, file_list)
        case "task":
            task = kwargs.get("task")
            system_prompt = get_task_prompt(task)
            llm_cfg = _get_llm_cfg(model_name, model_server, api_key, 0.8)
            print(f"task prompt {system_prompt}")
            return _get_basic_assistant(system_prompt, llm_cfg, [])


def _get_react_agent(system_prompt, tool_list, llm_cfg):
    _react_agent = ReActChat(
    #_react_agent = Assistant(
        function_list=tool_list,
        llm=llm_cfg,
        system_message=system_prompt
    )
    return _react_agent


def _get_basic_assistant(system_prompt, llm_cfg, file_list):
    _assistant = Assistant(
        llm=llm_cfg,
        system_message=system_prompt,
        files=file_list
    )
    return _assistant


def _get_llm_cfg(_model_name, _model_server, _api_key, _temperature):
    llm_cfg = {
        'model': _model_name,
        'model_server': _model_server,
        'api_key': _api_key,
        'generate_cfg': {
            'top_p': 0.8,
            'max_input_tokens': 24800,
            'temperature': _temperature
        }
    }
    return llm_cfg
