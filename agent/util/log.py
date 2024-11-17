import logging.handlers
import os


def get_uvicorn_log_handler(use_formatter):
    if os.environ.get("LOG_SYSLOG") == "enabled":
        syslog_host = os.environ.get("LOG_SYSLOG_HOST")
        syslog_port = os.environ.get("LOG_SYSLOG_PORT")
        return {
            "formatter": use_formatter,
            "class": "logging.handlers.SysLogHandler",
            "address": [syslog_host, int(syslog_port)],
            "facility": logging.handlers.SysLogHandler.LOG_LOCAL4
        }
    else:
        return None


def get_uvicorn_log_default_formatter():
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    if os.environ.get("LOG_SYSLOG") == "enabled":
        syslog_tag = os.environ.get("LOG_SYSLOG_TAG")
        return {"format": f"{syslog_tag}: {log_format}"}
    else:
        return None


def get_uvicorn_log_access_formatter():
    access_log_format = "%(asctime)s - %(levelprefix)s  %(client_addr)s - \"%(request_line)s\" %(status_code)s"
    if os.environ.get("LOG_SYSLOG") == "enabled":
        syslog_tag = os.environ.get("LOG_SYSLOG_TAG")
        return {'()': 'uvicorn.logging.AccessFormatter',
                "fmt": f"{syslog_tag}: {access_log_format}"}
    else:
        return None


log = logging.getLogger("uvicorn")
