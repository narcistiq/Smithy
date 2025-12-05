from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import CraftingRecipe, Item, UserList
from .serializer import ItemSerializer
from typing import Optional
import logging


def combineItems(item1, item2) -> Optional[Item]:
    try:
        query = Q(item_a=item1, item_b=item2) | Q(item_a=item2, item_b=item1)
        return CraftingRecipe.objects.get(query).result
    except CraftingRecipe.DoesNotExist:
        return None


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    UserList.objects.get_or_create(user=user)
    token, _ = Token.objects.get_or_create(user=user)

    return Response({"message": "User registered", "token": token.key}, status=201)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Invalid credentials"}, status=401)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"message": "Login successful", "token": token.key})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.auth.delete()
    return Response({"message": "Logged out"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    profile = UserList.objects.get(user=request.user)
    items = profile.discovered_items.all()

    return Response({
        "username": request.user.username,
        "discovered_items": [{"id": i.id, "name": i.name, "category": i.category} for i in items],
        "count": items.count()
    })


@api_view(['GET'])
def get_all_items(request):
    return Response(ItemSerializer(Item.objects.all(), many=True).data)


@api_view(['GET'])
def get_all_recipes(request):
    recipes = CraftingRecipe.objects.all()
    return Response([{
        "id": r.id,
        "item_a": r.item_a.name,
        "item_b": r.item_b.name,
        "result": r.result.name
    } for r in recipes])


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def combine_items(request):
    item1_name = request.data.get('item1_name')
    item2_name = request.data.get('item2_name')

    try:
        item1 = Item.objects.get(name__iexact=item1_name)
        item2 = Item.objects.get(name__iexact=item2_name)
    except Item.DoesNotExist:
        return Response({"error": "Invalid item"}, status=404)

    result = combineItems(item1, item2)
    if not result:
        return Response({"message": "Nothing created"})

    profile = UserList.objects.get(user=request.user)

    if profile.discovered_items.filter(id=result.id).exists():
        return Response({"message": f"You already discovered {result.name}", "is_new": False})

    profile.discovered_items.add(result)
    return Response({"message": f"New discovery: {result.name}", "is_new": True})