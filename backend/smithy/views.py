from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CraftingRecipe, Item
from .serializer import UserSerializer
# Create your views here.


def combineItems(item1, item2):
    try:
        query = Q(item_a=item1, item_b=item2) | Q(item_a=item2, item_b=item1)
        recipe = CraftingRecipe.objects.get(query)
        return recipe.result
    except CraftingRecipe.DoesNotExist:
        return None

@api_view(['GET'])
def get_user(request):
    return Response(UserSerializer({'name'}))