import pymysql


def get_query_data_list(sql: str, db_conn: pymysql.Connection = None) -> list[dict]:
    if db_conn is None:
        from agent.db import db_conn
    cursor = db_conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_table_ddl(table_name: str, db_conn: pymysql.Connection = None) -> str:
    get_ddl_sql = f"SHOW CREATE TABLE {table_name}"
    if db_conn is None:
        from agent.db import db_conn
    cursor = db_conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute(get_ddl_sql)
        result = cursor.fetchone()
        return result["Create Table"]
    except Exception as e:
        print(e)
        return ""


def get_schema_prompt(meta_db_conn, table_list):
    prompt = ""
    for table_meta in table_list:
        table_meta_dict = get_schema_by_meta(table_meta, meta_db_conn)
        for table in table_meta_dict.values():
            table_name = table.get("object_alias")
            table_desc = table.get("object_name")
            prompt += f"{table_desc} 表名 {table_name} ，结构如下: \n"
            table_fields = table.get("fields")
            for field in table_fields:
                prompt += f"- {field['alias']} {field['type']}: {field['name']} \n"
        prompt += "\n"
    return prompt


def get_schema_by_meta(alias, db_conn: pymysql.Connection, simple_type=True):
    sql = f""" SELECT o.`alias` as object_alias, o.`name` as object_name,f.`name`,f.`alias`,f.`type`,f.`max_length`,
    f.`max_num`,f.`max_size`,f.`max_value`,f.`precision` FROM meta_object_fields f LEFT JOIN meta_objects o ON 
    f.`object_id`=o.`id` WHERE o.`alias` LIKE "%{alias}"
    """
    cursor = db_conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    schema_mapping = {}
    for field in result:
        object_alias = field.get("object_alias").replace("VIEW_", "").replace("STAT_", "")
        object_name = field.get("object_name")
        if schema_mapping.get(object_alias):
            fields = schema_mapping.get(object_alias).get("fields")
        else:
            fields = []
            schema_mapping[object_alias] = {
                "object_name": object_name,
                "object_alias": object_alias,
                "fields": fields
            }

        field_type = int(field['type'])
        fields.append({
            "alias": field['alias'],
            "name": field['name'],
            "type":  get_simple_sql_type(field_type) if simple_type else field_type
        })
    return schema_mapping


def get_simple_sql_type(field_type):
    if field_type == 1 or field_type == 2:
        return " (VARCHAR) "
    elif field_type == 3:
        return " (NUMBER) "
    elif field_type == 4:
        return " (DATE) "
    elif field_type == 5:
        return " (DATETIME) "
    return " (VARCHAR) "
