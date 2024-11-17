import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    import uvicorn
    from fastapi.staticfiles import StaticFiles
    from api.api_v1 import app
    from uvicorn.config import LOGGING_CONFIG
    from agent.util.log import get_uvicorn_log_handler, get_uvicorn_log_default_formatter, \
        get_uvicorn_log_access_formatter

    uvicorn_log_default_formatter = get_uvicorn_log_default_formatter()
    if uvicorn_log_default_formatter is not None:
        LOGGING_CONFIG["formatters"]["default"] = uvicorn_log_default_formatter
    uvicorn_log_access_formatter = get_uvicorn_log_access_formatter()
    if uvicorn_log_access_formatter is not None:
        LOGGING_CONFIG["formatters"]["access"] = uvicorn_log_access_formatter
    default_log_handler = get_uvicorn_log_handler("default")
    if default_log_handler is not None:
        LOGGING_CONFIG["handlers"]["default"] = default_log_handler
    access_log_handler = get_uvicorn_log_handler("access")
    if access_log_handler is not None:
        LOGGING_CONFIG["handlers"]["access"] = access_log_handler
    print(LOGGING_CONFIG)
    chart_dir = os.environ.get("CHART_DIR")
    chart_uri = os.environ.get("CHART_URI")
    app.mount(
        chart_uri,
        StaticFiles(directory=chart_dir),
        name='chart',
    )
    app.mount("/ai/agent/statics/swagger-ui", StaticFiles(directory="statics/swagger-ui"), name='statics')
    uvicorn.run(app, host="0.0.0.0", port=8000)
