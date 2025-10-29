from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import CraftingRecipe, Item, UserList
from .serializer import UserSerializer
# Create your views here.


def get_guest_profile():
    guest_user = User.objects.get(username="guest")
    return UserList.objects.get(user=guest_user)


def combineItems(item1, item2):
    try:
        query = Q(item_a=item1, item_b=item2) | Q(item_a=item2, item_b=item1)
        recipe = CraftingRecipe.objects.get(query)
        if (recipe.discovered):
            return "Duplicate item"

        recipe.discovered = True  # switch boolean flag to prevent duplicates, hence the if recipe.discovered == true
        recipe.save()
        return recipe.result
    except CraftingRecipe.DoesNotExist:
        return None


def addItem(item1, item2):
    res = combineItems(item1, item2)
    if (res is None):
        return  
    guest_profile = get_guest_profile()

    guest_profile.discovered_items.add(res)


@api_view(['GET'])
def get_user(request):
    return Response(UserSerializer({'name'}))
