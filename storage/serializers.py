# coding=utf-8
from rest_framework_mongoengine.serializers import DocumentSerializer, DynamicDocumentSerializer

from storage.models import StorageGroup # ,StorageLayer

class StorageGroupSerializer(DynamicDocumentSerializer):
    class Meta:
        model = StorageGroup
        exclude = ('ctime', 'utime')
