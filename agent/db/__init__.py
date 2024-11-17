import json
import os

import pymysql
import requests
from pymysql import Connection

_db_host = os.environ.get("DATABASE_HOST")
_db_user = os.environ.get("DATABASE_USER")
_db_pwd = os.environ.get("DATABASE_PWD")
_db_port = int(os.environ.get("DATABASE_PORT"))
_db_name = os.environ.get("DATABASE_NAME")
_db_provider_url = os.environ.get("DATABASE_PROVIDER_URL")
db_conn = pymysql.connect(host=_db_host, user=_db_user, password=_db_pwd, port=_db_port,
                          database=_db_name)


def get_app_db_conn(app_id, db_type="app") -> Connection:
    if app_id == "66c59c9ad1a53a49798957fe":
        db_info = {
            "data": {
                "app": {
                    "addr": "rm-uf6l64g74yzw3i0jdao.mysql.rds.aliyuncs.com:3306",
                    "user": "test_user",
                    "pwd": "zxr@test",
                    "database": "test_app"
                },
                "meta": {
                    "addr": "rm-uf6l64g74yzw3i0jdao.mysql.rds.aliyuncs.com:3306",
                    "user": "test_user",
                    "pwd": "zxr@test",
                    "database": "test_meta"
                }
            }
        }
    else:
        db_data = requests.get(_db_provider_url, params={"app_id": app_id})
        db_data.raise_for_status()
        db_info = json.loads(db_data.text)
    if db_type == "app":
        db_conn_info = db_info['data']['app']
    elif db_type == "meta":
        db_conn_info = db_info['data']['meta']
    else:
        raise TypeError("invalid db type " + db_type)
    _app_db_addr = db_conn_info['addr'].split(":")
    _app_db_user = db_conn_info['user']
    _app_db_pwd = db_conn_info['pwd']
    _app_db_name = db_conn_info['database']
    _db_connection = pymysql.connect(host=_app_db_addr[0],
                                     user=_app_db_user,
                                     password=_app_db_pwd,
                                     port=int(_app_db_addr[1]),
                                     database=_app_db_name)
    return _db_connection
