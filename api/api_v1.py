import json

from fastapi import Request
from fastapi.responses import StreamingResponse

from agent.llm.llm_agent import get_agent
from agent.task.task_eval import task_val, parse_task_content
from agent.util.json_util import extract_json_from_md
from agent.util.log import log
from api import app
from api.doc_helper.api_v1 import get_chat_extra, get_history_extra, get_chat_stream_extra, get_task_extra

app.state.app_id = ""
app.state.app_version_id = ""
app.state.ide_login_id = ""


def _parse_react_response(text):
    special_thought_token = "Thought:"
    special_func_token = 'Action:'
    special_args_token = 'Action Input:'
    special_obs_token = 'Observation:'
    special_final_token = 'Final Answer:'
    # html_token = '```html'
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    for i, line in enumerate(lines):
        if (special_func_token in line
                or special_args_token in line
                or special_obs_token in line
                or special_thought_token in line):
            line = ""
        elif special_final_token in line:
            line = line.replace(special_final_token, "")
        # elif html_token in line:
        #     line = gr.HTML(line.replace(html_token,""))
        #     print("html line",line)
        lines[i] = "\n" + line
    text = "".join(lines)
    return text


def _filter_react_text(text: str) -> str:
    special_final_token = 'Final Answer:'
    text_arr = text.split(special_final_token)
    if len(text_arr) > 1:
        return text_arr[1]
    return text


@app.post(path="/ai/agent/v1/chat",
          summary="Chat with ai agent",
          description="跟AI 交互接口",
          openapi_extra=get_chat_extra()
          )
async def chat(request: Request):
    _history = []
    _request_data = await request.json()
    log.info(f"request.json : {_request_data}")
    message = _request_data.get("message")
    chat_type = _request_data.get("chat_type")
    if chat_type == "rag":
        if request.session is not None and "rag_chat_history" in request.session:
            _history = request.session.get("rag_chat_history")
    else:
        if request.session is not None and "ai_agent_chat_history" in request.session:
            _history = request.session.get("ai_agent_chat_history")
    app_id = _request_data.get("app_id")
    app_version_id = _request_data.get("app_version_id")
    app.state.app_id = app_id
    app.state.app_version_id = app_version_id
    app.state.ide_login_id = _request_data.get("login_id")
    agent_bot = get_agent(chat_type)
    log.info(f"User: {message}")
    query = {'role': 'user', 'content': message}
    _history.append(query)
    response = agent_bot.run_nonstream(_history)
    full_response = response[0]["content"]
    log.info(f"Qwen-Chat: {full_response}")
    filter_response = full_response
    if chat_type == "rag":
        filter_response = _filter_react_text(full_response)
    response[0]["content"] = filter_response
    _history.extend(response)
    log.info(f"History :{_history}")
    if request.session is not None:
        if chat_type == "rag":
            request.session.update({"rag_chat_history": _history})
        else:
            request.session.update({"ai_agent_chat_history": _history})
    return {"response": filter_response}


@app.get(path="/ai/agent/v1/history",
         summary="Get chat history",
         description="获取聊天记录",
         openapi_extra=get_history_extra()
         )
def get_chat_history(request: Request):
    chat_type = request.query_params.get("chat_type")
    _history = []
    if chat_type == "rag":
        if request.session is not None and "rag_chat_history" in request.session:
            _history = request.session.get("rag_chat_history")
    elif chat_type in ["app_agent", "ide_agent"]:
        if request.session is not None and "ai_agent_chat_history" in request.session:
            _history = request.session.get("ai_agent_chat_history")
    else:
        log.error(f"bad chat_type {chat_type} in get_chat_history ")
    return {"response": _history}


@app.post(path="/ai/agent/v1/chat/stream",
          summary="Chat with agent(stream) ",
          description="Stream 交互接口",
          openapi_extra=get_chat_stream_extra()
          )
async def stream_json(request: Request):
    _history = []
    _request_data = await request.json()
    log.info(f"request.json : {_request_data}")
    message = _request_data.get("message")
    rag = _request_data.get("rag")
    if rag is None:
        if request.session is not None and "ai_agent_chat_history" in request.session:
            _history = request.session.get("ai_agent_chat_history")
        app_id = _request_data.get("app_id")
        app_version_id = _request_data.get("app_version_id")
        app.state.app_id = app_id
        app.state.app_version_id = app_version_id
        app.state.ide_login_id = _request_data.get("login_id")
        agent_bot = get_agent("agent")
    else:
        if request.session is not None and "rag_chat_history" in request.session:
            _history = request.session.get("rag_chat_history")
        agent_bot = get_agent("rag")
    log.info(f"User: {message}")
    query = {'role': 'user', 'content': message}
    _history.append(query)

    def chat_stream(agent, history):
        for response in agent.run(history):
            full_response = _parse_react_response(response[0]["content"])
            yield from full_response
        _history.extend(response)
        log.info(f"History :{_history}")
        log.info(f"Qwen-Chat: {full_response}")
        if request.session is not None:
            if rag is None:
                request.session.update({"ai_agent_chat_history": _history})
            else:
                request.session.update({"rag_chat_history": _history})

    return StreamingResponse(chat_stream(agent_bot, _history), media_type="text/plain")


@app.post(path="/ai/agent/v1/task",
          summary="Task by model",
          description="任务接口，通过自然语言识别任务进行处理",
          openapi_extra=get_task_extra()
          )
async def task(request: Request):
    _request_data = await request.json()
    log.info(f"request.json : {_request_data}")
    task_name = _request_data.get("task_name")
    message = _request_data.get("content")
    event_args = _request_data.get("event_args")
    try:
        agent_bot = get_agent("task", task=task_name)
        _history = []
        interact_content = parse_task_content(task_name, message)
        query = {'role': 'user', 'content': interact_content}
        print(f"User query: {query}")
        _history.append(query)
        response = agent_bot.run_nonstream(_history)
        full_response = response[0]["content"]
        print(f"Qwen-Chat: {full_response}")
        filter_response = extract_json_from_md(full_response)
        result = task_val(task_name, filter_response, event_args)
        print(f"parse task json {filter_response} result {result}")
        return {"response": filter_response}
    except Exception as e:
        log.error(f"Exception {e}")
