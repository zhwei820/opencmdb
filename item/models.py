# coding=utf-8
from arch.models import Group
from django.db import models
from django_mongoengine import Document, DynamicDocument, fields
import datetime


# Create your models here.
class ItemCategory(Document):  #CI 模型定义
    name = fields.StringField(max_length=200, required=True)
    # name = fields.StringField(max_length=200, required=True, unique_with='group')
    group = fields.ReferenceField('Group')
    structure = fields.DictField()
    ctime = fields.DateTimeField(default=datetime.datetime.now())
    utime = fields.DateTimeField(default=datetime.datetime.now())

    meta = {
        "collection": "item_category",
        "indexes": [
            "name",
            # "$name",
            "ctime",
        ],
    }


class Item(DynamicDocument): # CI 模型实例
    name = fields.StringField(max_length=200, required=True)
    group = fields.ReferenceField('Group', required=True)
    category = fields.ReferenceField(ItemCategory, required=True)
    ctime = fields.DateTimeField(default=datetime.datetime.now())
    utime = fields.DateTimeField(default=datetime.datetime.now())

    meta = {
        "collection": "item",
        "indexes": [
            "category",
            "ctime",
        ],
    }
