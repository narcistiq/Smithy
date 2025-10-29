from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import CraftingRecipe, Item, UserList
from .serializer import UserSerializer
from typing import Optional
# Create your views here.


def get_guest_profile():
    guest_user = User.objects.get(username="guest")
    return UserList.objects.get(user=guest_user)


def combineItems(item1, item2) -> Optional[Item]:
    try:
        query = Q(item_a=item1, item_b=item2) | Q(item_a=item2, item_b=item1)
        recipe = CraftingRecipe.objects.get(query)
        return recipe.result
    except CraftingRecipe.DoesNotExist:
        return None


def addItem(item1, item2):
    res = combineItems(item1, item2)
    if (res is None):
        return  
    guest_profile = get_guest_profile()

    guest_profile.discovered_items.add(res)

# says request is nawt used
@api_view(['GET'])
def get_user(request):
    return Response(UserSerializer({'name'}))

@api_view(['POST'])
def combine_items(request):
    item1_check = request.data.get('item1_name')
    item2_check = request.data.get('item2_name')
    
    try:
        item1 = Item.objects.get(name=item1_check)
        item2 = Item.objects.get(name=item2_check)
    except Item.DoesNotExist:
        return Response(
            {"error": "One or both items do not exist."},
            status=status.HTTP_404_NOT_FOUND            
        )
    result_item = combineItems(item1, item2)
    if result_item is None:
        return Response(
            {"message": "These items don't create anything new."},
            status=status.HTTP_200_OK
        )  
    guest_profile = get_guest_profile()
    if guest_profile is None:
        return Response(
            {"error": "Guest profile not found."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    # 5. Add to discovered_items and check for duplicates
    # .add() is smart and won't create a duplicate entry
    if guest_profile.discovered_items.filter(pk=result_item).exists():
        message = f"You already discovered {result_item.name}!"
        is_new_discovery = False
    else:
        # This is the "addItem" logic, now in the right place
        guest_profile.discovered_items.add(result_item)
        message = f"New discovery! You made {result_item.name}!"
        is_new_discovery = True
    # 6. Return a successful JSON response
    return Response({
        "message": message,
        "new_item": result_item.name,
        "is_new": is_new_discovery
        }, status=status.HTTP_200_OK)