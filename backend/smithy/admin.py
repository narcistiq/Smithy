from django.contrib import admin

# Register your models here.
from .models import Item, CraftingRecipe

admin.site.register(Item)
admin.site.register(CraftingRecipe)

# declare models here, import them at top then register