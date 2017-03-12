# coding=utf-8
from rest_framework_mongoengine.serializers import DocumentSerializer

from arch.models import Layer, Group


class LayerSerializer(DocumentSerializer):
    class Meta:
        model = Layer
        exclude = ('ctime', 'utime')


class GroupSerializer(DocumentSerializer):
    class Meta:
        model = Group
        exclude = ('ctime', 'utime')
