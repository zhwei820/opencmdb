# coding=utf-8
import datetime

from item.models import ItemCategory, Item
import re

from jsonschema import validate
import json


def validate_item_field(attr_value, attr_form):
    """
    :param attr_value: item的属性
    :param attr_form: item category的属性规则
    :return:
    """
    if not isinstance(attr_form, dict):
        return -1, {"error": "attr_form is not a dict."}
    required = attr_form.get('required')
    if required == 'false':
        return 0, {"msg": "success"}
    field = attr_form.get('field')
    if not field:
        return -1, {"error": "field missed."}
    if field == "string":
        if not isinstance(attr_value, str):
            return -1, {"error": "attr_value is not a string."}
        if len(attr_value) < int(attr_form["min_length"]) or len(attr_value) > int(attr_form["max_length"]):
            return -1, {"error": "invalid string length."}
        if attr_form.get('valid_rule') == "none":
            return 0, {"msg": "success"}
        elif attr_form.get('valid_rule') == "IPaddress":
            pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')  # 匹配IP地址有待改进
        elif attr_form.get('valid_rule') == "email":
            pattern = re.compile(r'^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$')
        elif attr_form.get('valid_rule') == "phone":
            pattern = re.compile(r'^\d{11}$')
        else:
            return -1, {"error": "invalid valid_rule."}
        match = pattern.match(attr_value)
        if not match:
            return -1, {"error": "did not match rule: %s" % attr_form.get('valid_rule')}
    elif field == "text":
        if not isinstance(attr_value, str):
            return -1, {"error": "attr_value is not a string."}
        if len(attr_value) < int(attr_form["min_length"]) or len(attr_value) > int(attr_form["max_length"]):
            return -1, {"error": "invalid string length."}
    elif field == "select":
        if not isinstance(attr_value, str):
            return -1, {"error": "attr_value is not a dict."}
        if attr_value not in attr_form["choice"][1:-1].split("|"):
            return -1, {"error": "invalid choice."}
    elif field == "multiple_select":
        if not isinstance(attr_value, str):
            return -1, {"error": "attr_value is not a dict."}
        for each in attr_value.split("|"):
            if each not in attr_form["choice"][1:-1].split("|"):
                return -1, {"error": "invalid choice."}
    elif field == "integer":
        if not isinstance(attr_value, int):
            return -1, {"error": "attr_value is not a integer."}
        if attr_value < int(attr_form["min_value"]) or attr_value > int(attr_form["max_value"]):
            return -1, {"error": "invalid integer value."}
    elif field == "datetime":
        if not isinstance(attr_value, str):
            return -1, {"error": "attr_value is not a string."}
        try:
            date_object = datetime.datetime.strptime(
                attr_value, '%Y%m%d%H%M%S')
        except ValueError:
            return -1, {"error": "time data '%s' does not match format" % attr_value}
    elif field == "reference":
        if not isinstance(attr_value, str):
            return -1, {"error": "attr_value is not a string."}
        item_obj = Item.objects(id=attr_value)
        if not item_obj:
            return -1, {"error": "unknown item."}
        if item_obj.category.id != attr_form["reference"]:
            return -1, {"error": "wrong category."}

    return 0, {"msg": "success"}


_fields_comment = {
    'string': "单行文本",
    'text': "多行文本",
    'select': "单选",
    'multi_select': "多选",
    'image': "图片",
    'number': "数值",
    'datetime': "日期时间",
    'required': "是否必填",
    'name': "字段名称",
    'default': "默认",
    'max': "最大/最长",
    'min': "最小/最短",
    'unit': "单位",
    'choice': "选项(以|分割)",
    'field': "字段类型",
    'key': "关键词",
    'ref': "模型引用",
    'reference': "模型引用",


    # 'reference': {
    #     "required": r'^(True)|(False)$',
    #     "reference": r'^\w{24}$',
    # },  # 引用
    # 'image': {
    #     "required": r'^(True)|(False)$',
    # },  # 图片
}


# json_schema

_valid_fields = {
    'string': {
        "required": True,
        "type": "object",
        "id": "id",
        "properties": {
            "field": {
                "required": True,
                "type": "string",
                "id": "field"
            },
            "required": {
                "required": True,
                "type": "boolean",
                "id": "required"
            },
            "name": {
                "required": True,
                "type": "string",
                "id": "name"
            },
            "key": {
                "required": True,
                "type": "string",
                "id": "key"
            },
            "default":
            {
                "required": True,
                "type": "string",
                "id": "default",
                "maxLength": 100000,
                "minLength": 0,
            },
            "max": {
                "required": True,
                "type": "number",
                "id": "max",
                "minimum": 0
            },
            "min": {
                "required": True,
                "type": "number",
                "id": "max",
                "maximum": 100000000
            },
        }
    },
    'text': {
        "required": True,
        "type": "object",
        "id": "id",
        "properties": {
            "field": {
                "required": True,
                "type": "string",
                "id": "field"
            },
            "required": {
                "required": True,
                "type": "boolean",
                "id": "required"
            },
            "name": {
                "required": True,
                "type": "string",
                "id": "name"
            },
            "key": {
                "required": True,
                "type": "string",
                "id": "key"
            },
            "default":
            {
                "required": True,
                "type": "string",
                "id": "default"
            },
        }
    },
    'number': {
        "required": True,
        "type": "object",
        "id": "id",
        "properties": {
            "field": {
                "required": True,
                "type": "string",
                "id": "field"
            },
            "required": {
                "required": True,
                "type": "boolean",
                "id": "required"
            },
            "name": {
                "required": True,
                "type": "string",
                "id": "name"
            },
            "key": {
                "required": True,
                "type": "string",
                "id": "key"
            },
            "max": {
                "required": True,
                "type": "number",
                "id": "max",
                "minimum": 0
            },
            "min": {
                "required": True,
                "type": "number",
                "id": "max",
                "maximum": 100000000
            },
            "unit": {
                "required": True,
                "type": "string",
                "id": "unit"
            },
            "default":
            {
                "required": True,
                "type": "number",
                "id": "default",
                "maximum": 100000000,
                "minimum": 0

            },
        }
    },
    "select": {
        "required": True,
        "type": "object",
        "id": "machine_type",
        "properties": {
            "field": {
                "required": True,
                "type": "string",
                "id": "field"
            },
            "required": {
                "required": True,
                "type": "boolean",
                "id": "required"
            },
            "name": {
                "required": True,
                "type": "string",
                "id": "name"
            },
            "key": {
                "required": True,
                "type": "string",
                "id": "key"
            },
            "choice": {
                "required": True,
                "type": "string",
                "id": "choice",
                "pattern": r'^(.+|)*(.+)$'
            }
        }
    },
    "multi_select": {
        "required": True,
        "type": "object",
        "id": "machine_type",
        "properties": {
            "field": {
                "required": True,
                "type": "string",
                "id": "field"
            },
            "required": {
                "required": True,
                "type": "boolean",
                "id": "required"
            },
            "name": {
                "required": True,
                "type": "string",
                "id": "name"
            },
            "key": {
                "required": True,
                "type": "string",
                "id": "key"
            },
            "choice": {
                "required": True,
                "type": "string",
                "id": "choice",
                "pattern": r'^(.+|)*(.+)$'
            }
        }
    },
    "datetime": {
        "required": True,
        "type": "object",
        "id": "machine_type",
        "properties": {
            "field": {
                "required": True,
                "type": "string",
                "id": "field"
            },
            "required": {
                "required": True,
                "type": "boolean",
                "id": "required"
            },
            "name": {
                "required": True,
                "type": "string",
                "id": "name"
            },
            "key": {
                "required": True,
                "type": "string",
                "id": "key"
            },
            # "choice": {
            #     "required": True,
            #     "type": "string",
            #     "id": "choice",
            #     "pattern":r'^(\d{2}|\d{4})(?:\-)?([0]{1}\d{1}|[1]{1}[0-2]{1})(?:\-)?([0-2]{1}\d{1}|[3]{1}[0-1]{1})(?:\s)?([0-1]{1}\d{1}|[2]{1}[0-3]{1})(?::)?([0-5]{1}\d{1})(?::)?([0-5]{1}\d{1})$'
            # }
        }
    },
    "image": {
        "required": True,
        "type": "object",
        "id": "image",
        "properties": {
            "field": {
                "required": True,
                "type": "string",
                "id": "field"
            },
            "required": {
                "required": True,
                "type": "boolean",
                "id": "required"
            },
            "name": {
                "required": True,
                "type": "string",
                "id": "name"
            },
            "key": {
                "required": True,
                "type": "string",
                "id": "key"
            },
            # "choice": {
            #     "required": True,
            #     "type": "string",
            #     "id": "choice",
            #     "pattern":r'^(\d{2}|\d{4})(?:\-)?([0]{1}\d{1}|[1]{1}[0-2]{1})(?:\-)?([0-2]{1}\d{1}|[3]{1}[0-1]{1})(?:\s)?([0-1]{1}\d{1}|[2]{1}[0-3]{1})(?::)?([0-5]{1}\d{1})(?::)?([0-5]{1}\d{1})$'
            # }
        }
    },
    "ref": {
            "required": True,
            "type": "object",
            "id": "image",
            "properties": {
                "field": {
                    "required": True,
                    "type": "string",
                    "id": "field"
                },
                "required": {
                    "required": True,
                    "type": "boolean",
                    "id": "required"
                },
                "name": {
                    "required": True,
                    "type": "string",
                    "id": "name"
                },
                "key": {
                    "required": True,
                    "type": "string",
                    "id": "key"
                },
                "reference": {
                    "required": True,
                    "type": "string",
                    "id": "key"
                },
                # "choice": {
                #     "required": True,
                #     "type": "string",
                #     "id": "choice",
                #     "pattern":r'^(\d{2}|\d{4})(?:\-)?([0]{1}\d{1}|[1]{1}[0-2]{1})(?:\-)?([0-2]{1}\d{1}|[3]{1}[0-1]{1})(?:\s)?([0-1]{1}\d{1}|[2]{1}[0-3]{1})(?::)?([0-5]{1}\d{1})(?::)?([0-5]{1}\d{1})$'
                # }
            }
        },
}



_valid_item_fields = {
    'string': {
        "required": True,
        "type": "string",
        "id": "id",
        "maxLength": 100000,
        "minLength": 0,
    },
    'text': {
        "required": True,
        "type": "string",
        "id": "id",
    },
    'number': {
        "required": True,
        "type": "string",
        "id": "id",
        "minimum": 0,
        "maximum": 0,
    },
    "select": {
        "required": True,
        "type": "string",
        "id": "machine_type",
    },
    "multi_select": {
        "required": True,
        "type": "string",
        "id": "machine_type",
    },
    "datetime": {
        "required": True,
        "type": "string",
        "id": "machine_type",
    },
    "image": {
        "required": True,
        "type": "string",
        "id": "machine_type",
    },
    "ref": {
        "required": True,
        "type": "string",
        "id": "machine_type",
    },
}


def gemerating_category_schema(s_data):
    json_schema = {
        "$schema": "http://json-schema.org/draft-03/schema#",
        "required": True,
        # "type": "object",
        "id": "#",
        "properties": {}
    }

    for data in s_data:
        attr_name = data.get("key")
        if not isinstance(data, dict):
            return -1, {"error": "Data is not a dict."}
        field = data.get("field")
        # print(attr_name)
        # print(field)
        if field not in _valid_fields:
            return -1, {"error": "Unknown attribute filed type."}
        schema_bean = _valid_fields[field]
        schema_bean['id'] = attr_name
        # print(schema_bean)

        _max = data.get("max", -10000)
        _min = data.get("min", -10000)
        if not _max or not _min or _max < _min:
            return -1, {"error": "%s maximum and mininum not correct." % (attr_name)}
        if _max > 0:
            schema_bean['properties']['min']['maximum'] = _max
            schema_bean['properties']['max']['mininum'] = _min
        if field == "number":
            schema_bean['properties']['default']['maximum'] = _max
            schema_bean['properties']['default']['mininum'] = _min
        if field == "string":
            schema_bean['properties']['default']['maxLength'] = _max
            schema_bean['properties']['default']['minLength'] = _min

        json_schema['properties'][attr_name] = schema_bean

    return 0, json_schema



def gemerating_item_schema(s_data):
    json_schema = {
        "$schema": "http://json-schema.org/draft-03/schema#",
        "required": True,
        # "type": "object",
        "id": "#",
        "properties": {
            "category": {
                "required": True, 
                "type": "string", 
                "id": "category"
            }, 
            "name": {
                "required": True, 
                "type": "string", 
                "id": "name"
            }, 
            "id": {
                "required": False, 
                "type": "string", 
                "id": "id"
            }, 
        }
    }

    for data in s_data:
        attr_name = data.get("key")
        if not isinstance(data, dict):
            return -1, {"error": "Data is not a dict."}
        field = data.get("field")
        if field not in _valid_item_fields:
            return -1, {"error": "Unknown attribute filed type."}
        schema_bean = _valid_item_fields[field]
        schema_bean['id'] = attr_name
        # print(schema_bean)

        _max = data.get("max", -10000)
        _min = data.get("min", -10000)
        if not _max or not _min or _max < _min:
            return -1, {"error": "%s maximum and mininum not correct." % (attr_name)}
        if field == "number":
            schema_bean['maximum'] = _max
            schema_bean['mininum'] = _min
        if field == "string":
            schema_bean['maxLength'] = _max
            schema_bean['minLength'] = _min

        json_schema[attr_name] = schema_bean

    return 0, json_schema


from item.serializers import ItemCategorySerializer, ItemSerializer


def validate_item_structure(data):
    """
    :param data: 待验证的Item数据，是一个dict
    :return:
    """
    if not isinstance(data, dict):
        return -1, {"error": "Data is not a dict."}
    category = data.get("category")
    if not category:
        return -1, {"error": "Category is not defined."}
    item_category_object = ItemCategory.objects.get(id=category)
    if not item_category_object:
        return -1, {"error": "Category does not exists."}

    serializer = ItemCategorySerializer(item_category_object)
    struct = []
    for k in serializer.data['structure']:
        if k == 'hidden':
            continue
        for v in serializer.data['structure'][k]:
            if len(v) > 0:
                struct.append(v)

    json_shema_res = gemerating_item_schema(struct)
    if json_shema_res[0] < 0:
        return -1, json_shema_res[1]
    try:
        # print(json_shema_res)
        validate(data, json_shema_res[1])
    except Exception as e:
        print(e)
    else:
        print("json good")

    return 0, {"msg": "success"}

    for attr_group_name, attr_group_value in field_data.items():
        if attr_group_name not in item_category_object.structure:
            return -1, {"error": "Invaild attr_group:%s" % attr_group_name}
        for attr_name, attr_value in attr_group_value.items():
            if attr_name not in item_category_object.structure[attr_group_name]:
                return -1, {"error": "Invaild attr:%s" % attr_name}
            state, msg = validate_item_field(attr_value, item_category_object.structure[
                                             attr_group_name][attr_name])
            if state != 0:
                return state, msg
    return 0, {"msg": "success"}


def validate_category_structure(raw_data):  # 检验模型定义字段
    structure = raw_data.get("structure")
    if not structure:
        return -1, {"error": "raw Data missed attr: structure"}
    if not isinstance(structure, dict):
        return -1, {"error": "structure is not a dict."}

    for cpg_index in structure:
        if cpg_index == "hidden":
            continue
        s_data = structure[cpg_index]
        if not isinstance(s_data, list):
            return -1, {"error": "s_data is not a dict."}

        json_shema_res = gemerating_category_schema(s_data)
        if json_shema_res[0] < 0:
            return -1, json_shema_res[1]
        try:
            validate(s_data, json_shema_res[1])
        except Exception as e:
            print(e)
        else:
            print("json good")
        for data in s_data:
            attr_name = data.get("key")
            field = data.get("field")
            if field == 'reference':
                item_category_obj = ItemCategory.objects(id=field["reference"])
                if not item_category_obj:
                    return -1, {"error": "unknown reference."}

    return 0, {"msg": "success"}


# structure = {
#     "default": [
#          {
#             "key":"ip",
#             "name": "ip地址",
#             "field": "string",
#             "min": 1,
#             "max": 200,
#             "default": "1000",
#             "required": True
#         },
#          {
#             "key":"cpu",
#             "name": "cpu",
#             "field": "string",
#             "max": 200,
#             "min": 1,
#             "default": "1000",
#             "required": True
#         },
#         {
#             "key":"memory",
#             "name": "内存",
#             "field": "number",
#             "min": 10,
#             "max": 200,
#             "required": True,
#             "unit":"Gb",
#             "default": 100,
#         },
#         {
#             "key":"machine_type",
#             "name": "机器类型",
#             "field": "select",
#             "required": True,
#             "choice": "虚拟机|物理机|云主机",
#         },
#         {
#             "key":"mul_test",
#             "name": "机器类型",
#             "field": "multi_select",
#             "required": True,
#             "choice": "test1|test2|test3",
#         },
#         {
#             "key":"buytime",
#             "name": "购买日期",
#             "field": "datetime",
#             "required": True,
#         },
#     ]
# }
# s_data = structure['default']
# json_shema = gemerating_category_schema(s_data)

# print(json.dumps(json_shema[1]))

# try:
#     validate(s_data, json_shema[1])
# except Exception as e:
#     print(e.message)
# else:
#     print("json good")


# print(validate_category_structure({"structure":structure}))


s_data1 = {"name": "234", "id": "", "category": "58953a76cc8b7914090dea76",
           "size": "1", "ip": "127.0.0.1", "port": "3307"}

s_data = [
    {
        "required": "",
        "default": "1",
        "name": "size",
        "field": "number",
        "min": 1,
        "unit": "a",
        "key": "size",
        "max": 1
    },
    {
        "required": "",
        "default": "127.0.0.1",
        "key": "ip",
        "name": "ip",
        "max": 20,
        "field": "string",
        "min": 1
    },
    {
        "required": "",
        "default": "3307",
        "name": "端口",
        "field": "number",
        "min": 4,
        "unit": "",
        "key": "port",
        "max": 8
    }
]

json_shema = gemerating_item_schema(s_data)

# print(json.dumps(json_shema[1]))

try:
    validate(s_data1, json_shema[1])
except Exception as e:
    print(e.message)
else:
    print("json good")

# print(validate_item_structure(s_data1))
