# coding=utf-8
from arch.models import Layer, Group
from item.models import ItemCategory


class SidebarMixin(object):

    def get_context_data(self, **kwargs):
        context = super(SidebarMixin, self).get_context_data(**kwargs)
        layers = {}
        layer_collection = Layer.objects()
        for layer in layer_collection:
            layers[layer.name] = {}
            group_collection = Group.objects(layer=layer.id)
            for group in group_collection:
                layers[layer.name][group.name] = []
                category_collection = ItemCategory.objects(group=group.id)
                for category in category_collection:
                    layers[layer.name][group.name].append(category.name)

        context["layers"] = layers
        return context
