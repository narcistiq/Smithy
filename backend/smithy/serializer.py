from rest_framework import serializers
from .models import Item, CraftingRecipe


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'category']


class CraftingRecipeSerializer(serializers.ModelSerializer):
    item_a_name = serializers.CharField(source='item_a.name', read_only=True)
    item_b_name = serializers.CharField(source='item_b.name', read_only=True)
    result_name = serializers.CharField(source='result.name', read_only=True)
    
    class Meta:
        model = CraftingRecipe
        fields = ['id', 'item_a_name', 'item_b_name', 'result_name', 'discovered']
