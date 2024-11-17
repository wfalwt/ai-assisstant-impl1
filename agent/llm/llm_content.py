from pydantic import BaseModel

from api.model.task.translation import Translation


def get_task_content(task: str, content: dict | str) -> BaseModel:
    match task:
        case 'translation':
            return Translation(**content)