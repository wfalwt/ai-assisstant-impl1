import pymysql

db_host = "rm-uf6l64g74yzw3i0jdao.mysql.rds.aliyuncs.com"
db_port = 3306
db_user = "test_user"
db_pwd = "zxr@test"
db_name = "test_meta"


def get_schema_by_meta(alias):
    sql = f"""
    SELECT o.`alias` as object_alias, o.`name` as object_name,f.`name`,f.`alias`,f.`type`,f.`max_length`,f.`max_num`,f.`max_size`,f.`max_value`,f.`precision` FROM meta_object_fields f LEFT JOIN meta_objects o ON f.`object_id`=o.`id`
WHERE o.`alias` LIKE "%{alias}"
    """

    db_conn = pymysql.connect(host=db_host, user=db_user, password=db_pwd, port=db_port,
                              database=db_name)
    cursor = db_conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    schema_mapping = {}
    for field in result:
        object_alias = field.get("object_alias")
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
            "type": get_simple_sql_type(field_type)
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


if __name__ == "__main__":
    table_list = ["erp_daily_putaway_report", "erp_daily_outbround_report", "erp_daily_inbround_report", "empty_position_data", "standard_inventory_age_report"]
    for table_meta in table_list:
        table_meta = get_schema_by_meta("erp_daily_putaway_report")
        for table in table_meta.values():
            table_name = table.get("object_alias")
            table_desc = table.get("object_name")
            print(f"{table_desc} 表名 {table_name} ，结构如下: ")
            table_fields = table.get("fields")
            for field in table_fields:
                print(f"- {field['alias']} {field['type']} : {field['name']} ")
        print("")