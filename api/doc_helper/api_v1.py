from api.model.v1.chat_model import ChatInput, ChatOutput, ChatHistory
from api.model.v1.task_model import TaskInput


def get_chat_extra():
    return {
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": ChatInput.model_json_schema()
                }
            },
            "required": True
        },
        "responses": {
            "200": {
                "description": "返回聊天内容",
                "content": {
                    "application/json": {
                        "schema": ChatOutput.model_json_schema()
                    }
                }
            }
        }
    }


def get_chat_stream_extra():
    return {
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": ChatInput.model_json_schema()
                }
            },
            "required": True
        },
        "responses": {
            "200": {
                "description": "返回聊天内容",
                "content": {
                    "text/plain": {
                        "schema": {
                            "type": "string",
                            "example": "This is a stream string from ai"
                        }
                    }
                }
            }
        }
    }


def get_history_extra():
    return {
        "parameters": [
            {
                "in": "query",
                "name": "chat_type",
                "required": True,
                "description": "聊天记录类型：ai_agent 表示跟AI Agent的聊天记录，rag 表示跟AI知识库的聊天记录",
                "schema": {
                    "type": "string",
                    "enum": ["ai_agent", "rag"]
                }
            }
        ],
        "responses": {
            "200": {
                "description": "返回聊天记录",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "response": {
                                    "description": "聊天记录",
                                    "type": "array",
                                    "items": ChatHistory.model_json_schema()
                                },
                            }
                        }
                    }
                }
            }
        }
    }


def get_task_extra():
    return {
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": TaskInput.model_json_schema()
                }
            },
            "required": True
        },
        "responses": {
            "200": {
                "description": "返回聊天内容",
                "content": {
                    "application/json": {
                        "schema": ChatOutput.model_json_schema()
                    }
                }
            }
        }
    }