from django.contrib import admin

# Register your models here.
from .models import Item, CraftingRecipe, NoDuplicate

admin.site.register(Item)
admin.site.register(CraftingRecipe)
admin.site.register(NoDuplicate)

# declare models here, import them at top then register