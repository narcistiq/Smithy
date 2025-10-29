from django.contrib import admin

# Register your models here.
from .models import Item, CraftingRecipe, UserList

admin.site.register(Item)
admin.site.register(CraftingRecipe)
admin.site.register(UserList)

# declare models here, import them at top then register