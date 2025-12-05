from django.contrib import admin
from .models import Item, CraftingRecipe, UserList

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name']
    list_filter = ['category']

@admin.register(CraftingRecipe)
class CraftingRecipeAdmin(admin.ModelAdmin):
    list_display = ['item_a', 'item_b', 'result', 'is_discovered']
    search_fields = ['item_a__name', 'item_b__name', 'result__name']
    def is_discovered(self, obj):
        return UserList.objects.filter(discovered_items=obj.result).exists()
    is_discovered.boolean = True   
    is_discovered.short_description = 'Discovered'

@admin.register(UserList)
class UserListAdmin(admin.ModelAdmin):
    list_display = ['user', 'discovered_items_count']
    search_fields = ['user__username']
    filter_horizontal = ['discovered_items']
    
    def discovered_items_count(self, obj):
        return obj.discovered_items.count()
    discovered_items_count.short_description = 'Discovered Items'