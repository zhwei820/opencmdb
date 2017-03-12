# coding=utf-8
import datetime

from rest_framework import status

from arch.models import Layer, Group
from arch.serializers import LayerSerializer, GroupSerializer
from django.shortcuts import render

from item.models import ItemCategory, Item


# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_mongoengine.generics import CreateAPIView, UpdateAPIView, RetrieveDestroyAPIView, ListAPIView, \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView


class LayerListCreateAPIView(ListCreateAPIView):
    serializer_class = LayerSerializer
    queryset = Layer.objects.all()
    permission_classes = (IsAuthenticated,)



class LayerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = LayerSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj_id = self.kwargs.get("id")
        return Layer.objects(id=obj_id).first()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if not instance:
            return Response({"error": "object does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if instance:
            instance.utime = datetime.datetime.now()
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({"error": "object does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        _obj_set = Group.objects(layer=instance)
        if _obj_set:
            return Response({"error": "can't delete this layer because it has group in it."},
                            status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class GroupListCreateAPIView(ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Group.objects.all()


class GroupRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj_id = self.kwargs.get("id")
        return Group.objects(id=obj_id).first()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if not instance:
            return Response({"error": "object does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if instance:
            instance.utime = datetime.datetime.now()
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({"error": "object does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        _obj_set = ItemCategory.objects(group=instance)
        if _obj_set:
            return Response({"error": "can't delete this group because it has category in it."},
                            status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupWithLayerIDListAPIView(ListAPIView):
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        obj_id = self.kwargs.get("id")
        return Group.objects(layer=obj_id)
