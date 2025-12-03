from django.contrib import admin
from .models import Item, CraftingRecipe, UserList

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name']
    list_filter = ['category']

@admin.register(CraftingRecipe)
class CraftingRecipeAdmin(admin.ModelAdmin):
    list_display = ['item_a', 'item_b', 'result', 'discovered']
    search_fields = ['item_a__name', 'item_b__name', 'result__name']
    list_filter = ['discovered']
    readonly_fields = ['discovered']

@admin.register(UserList)
class UserListAdmin(admin.ModelAdmin):
    list_display = ['user', 'discovered_items_count']
    search_fields = ['user__username']
    filter_horizontal = ['discovered_items']
    
    def discovered_items_count(self, obj):
        return obj.discovered_items.count()
    discovered_items_count.short_description = 'Discovered Items'