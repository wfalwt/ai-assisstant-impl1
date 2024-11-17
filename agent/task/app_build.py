from agent.tool.create_object import CreateObject
from api.model.task.app_schema import BusinessSystem


def app_build(system: BusinessSystem):
    for table in system.table_list:
        object_fields = []
        for table_field in table.table_fields:
            object_field = {
                "field_name": table_field.field_name,
                "field_alias": table_field.field_name,
                "field_type": table_field.field_type,
            }
            object_fields.append(object_field)

        object_params = {
            "object_name": table.table_name,
            "object_alias": table.table_name,
            "object_description": table.table_desc,
            "object_fields": object_fields
        }

        new_object = CreateObject()
        result = new_object.call(params=object_params)
