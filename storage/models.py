from django.db import models

# Create your models here.
from django_mongoengine import Document, DynamicDocument, fields
import datetime


class StorageGroup(DynamicDocument):  # storage 分组
    group = fields.ReferenceField('self', blank = True, null = True)
    name = fields.StringField(max_length=200, required=True)
    ctime = fields.DateTimeField(default=datetime.datetime.now())
    utime = fields.DateTimeField(default=datetime.datetime.now())

    meta = {
        "collection": "storagegroup",
        "indexes": [
            "name",
            "ctime",
        ],
    }
