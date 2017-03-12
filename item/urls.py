# coding=utf-8
from django.conf.urls import url
from django.contrib import admin

from item.views import ItemCategoryListCreateAPIView,\
    ItemCategoryRetrieveUpdateDestroyAPIView, ItemListCreateAPIView, ItemRetrieveUpdateDestroyAPIView, \
    ItemWithCategoryIDListAPIView, ItemCategoryWithGroupIDListAPIView, ItemWithCategoryIDListView, ItemDetailView, \
    CategoryEditView

urlpatterns = [
    url(r'^categories/(?P<id>\w{24})/items/$', ItemWithCategoryIDListView.as_view()),
    url(r'^items/(?P<id>\w{24})/', ItemDetailView.as_view()),
    url(r'^categories/(?P<id>\w{24})/', CategoryEditView.as_view()),
]
