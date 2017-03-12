# Create your views here.
import datetime

from rest_framework import status

from item.models import Item

# from storage.models import StorageLayer, StorageGroup
# from storage.serializers import StorageLayerSerializer, StorageGroupSerializer

from storage.models import StorageGroup
from storage.serializers import StorageGroupSerializer

from django.shortcuts import render


# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_mongoengine.generics import CreateAPIView, UpdateAPIView, RetrieveDestroyAPIView, ListAPIView, \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView


class StorageGroupListCreateAPIView(ListCreateAPIView):
    serializer_class = StorageGroupSerializer
    permission_classes = (IsAuthenticated,)
    queryset = StorageGroup.objects.all()


class StorageGroupRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = StorageGroupSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj_id = self.kwargs.get("id")
        return StorageGroup.objects(id=obj_id).first()

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
        _obj_set = StorageGroup.objects(group=instance)
        if _obj_set:
            return Response({"error": "can't delete this StorageGroup because it has items reserved."},
                            status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

