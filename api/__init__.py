import os

from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from redis import Redis
from starlette_session import BackendType
from starlette_session import SessionMiddleware


def swagger_ui_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url='/ai/agent/statics/swagger-ui/swagger-ui-bundle.js',
        swagger_css_url='/ai/agent/statics/swagger-ui/swagger-ui.css',
        swagger_favicon_url='/ai/agent/statics/swagger-ui/favicon.png',
    )


def redoc_ui_path(*args, **kwargs):
    return get_redoc_html(*args, **kwargs,
                          redoc_js_url='/ai/agent/statics/swagger-ui/redoc.standalone.js',
                          redoc_favicon_url='/ai/agent/statics/swagger-ui/favicon.png',
                          )


applications.get_swagger_ui_html = swagger_ui_patch
applications.get_redoc_html = redoc_ui_path

app = FastAPI(title="MindForce AI Assistant", docs_url="/ai/agent/docs", redoc_url="/ai/agent/redoc")
_redis_url = os.environ.get("REDIS_URL")
redis_client = Redis.from_url(_redis_url)

_secret_key = os.environ.get("API_SECRET_KEY")
_cookie_name = os.environ.get("API_COOKIE_NAME")
app.add_middleware(
    SessionMiddleware,
    secret_key=_secret_key,
    cookie_name=_cookie_name,
    backend_type=BackendType.redis,
    backend_client=redis_client
)
