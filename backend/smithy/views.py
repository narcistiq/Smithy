from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import CraftingRecipe, Item, UserList
from .serializer import ItemSerializer
from typing import Optional

@csrf_exempt
@api_view(['POST'])
def register(request):
    """Register a new user"""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {"error": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create user
    user = User.objects.create_user(
        username=username,
        email=email or '',
        password=password
    )
    
    # Create user profile
    user_profile, _ = UserList.objects.get_or_create(user=user)
    
    # Get or create token
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        },
        "token": token.key
    }, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['POST'])
def login(request):
    """Login user and return token"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {"error": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response(
            {"error": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Get or create token
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        },
        "token": token.key
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def logout(request):
    """Logout user - delete their token"""
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_200_OK
        )
    except Token.DoesNotExist:
        return Response(
            {"error": "Token not found."},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_user_profile(request):
    """Get current user's profile and discovered items"""
    if not request.user.is_authenticated:
        return Response(
            {"error": "Not authenticated."},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        user_profile = UserList.objects.get(user=request.user)
        discovered = user_profile.discovered_items.all()
        
        return Response({
            "user": {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email
            },
            "discovered_items": [
                {"id": item.id, "name": item.name, "category": item.category}
                for item in discovered
            ],
            "total_discovered": discovered.count()
        }, status=status.HTTP_200_OK)
    except UserList.DoesNotExist:
        return Response(
            {"error": "User profile not found."},
            status=status.HTTP_404_NOT_FOUND
        )


def get_guest_profile():
    """Get or create guest user profile"""
    guest_user, _ = User.objects.get_or_create(username="guest")
    user_profile, _ = UserList.objects.get_or_create(user=guest_user)
    return user_profile


def combineItems(item1, item2) -> Optional[Item]:
    """Check if two items can be combined and return result"""
    try:
        query = Q(item_a=item1, item_b=item2) | Q(item_a=item2, item_b=item1)
        recipe = CraftingRecipe.objects.get(query)
        return recipe.result
    except CraftingRecipe.DoesNotExist:
        return None


@api_view(['GET'])
def get_all_items(request):
    """Get all items in the game"""
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_recipes(request):
    """Get all crafting recipes"""
    recipes = CraftingRecipe.objects.all()
    recipe_data = []
    for recipe in recipes:
        recipe_data.append({
            "id": recipe.id,
            "item_a": recipe.item_a.name,
            "item_b": recipe.item_b.name,
            "result": recipe.result.name,
            "discovered": recipe.discovered
        })
    return Response(recipe_data)


@api_view(['GET'])
def get_user(request):
    """Get current user's discovered items"""
    guest_profile = get_guest_profile()
    discovered = guest_profile.discovered_items.all()
    serializer = ItemSerializer(discovered, many=True)
    return Response({
        "username": guest_profile.user.username,
        "discovered_items": serializer.data,
        "total_discovered": discovered.count()
    })


@csrf_exempt
@api_view(['POST'])
def combine_items(request):
    """Combine two items and return the result"""
    item1_check = request.data.get('item1_name')
    item2_check = request.data.get('item2_name')
    
    if not item1_check or not item2_check:
        return Response(
            {"error": "Both item1_name and item2_name are required."},
            status=status.HTTP_400_BAD_REQUEST            
        )
    
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
    
    # Check if already discovered
    if guest_profile.discovered_items.filter(pk=result_item).exists():
        message = f"You already discovered {result_item.name}!"
        is_new_discovery = False
    else:
        guest_profile.discovered_items.add(result_item)
        message = f"New discovery! You made {result_item.name}!"
        is_new_discovery = True
    
    return Response({
        "message": message,
        "new_item": result_item.name,
        "is_new": is_new_discovery
    }, status=status.HTTP_200_OK)