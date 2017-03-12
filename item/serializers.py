# coding=utf-8
from rest_framework_mongoengine.serializers import DocumentSerializer,\
    DynamicDocumentSerializer

from item.models import ItemCategory, Item


class ItemCategorySerializer(DocumentSerializer):
    class Meta:
        model = ItemCategory
        exclude = ('ctime', 'utime')


class ItemSerializer(DynamicDocumentSerializer):
    class Meta:
        model = Item
        exclude = ('ctime', 'utime')
