# coding=utf-8
from django.db import models
from django_mongoengine import Document, DynamicDocument, fields
import datetime


# Create your models here.
class Layer(Document): # CI 层
    name = fields.StringField(max_length=200, unique=True, required=True)
    ctime = fields.DateTimeField(default=datetime.datetime.now())
    utime = fields.DateTimeField(default=datetime.datetime.now())

    meta = {
        "collection": "layer",
        "indexes": [
            "name",
            # "$name",
            "ctime",
        ],
    }


class Group(Document):  # CI 分组
    name = fields.StringField(max_length=200, required=True, unique_with="layer")
    layer = fields.ReferenceField(Layer, required=True)
    ctime = fields.DateTimeField(default=datetime.datetime.now())
    utime = fields.DateTimeField(default=datetime.datetime.now())

    meta = {
        "collection": "group",
        "indexes": [
            "name",
            # "$name",
            "ctime",
        ],
    }
