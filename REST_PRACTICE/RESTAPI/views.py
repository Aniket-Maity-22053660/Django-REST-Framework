from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import MenuItemSerializer
from .models import MenuItems
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes, throttle_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
# Create your views here.

@api_view(['GET', 'POST'])
def books(request):
    return Response({"message" : 'list of the books'}, status=status.HTTP_200_OK)
def bookshttp(request):
    return HttpResponse("Viewing this via django.http!")

class BookList(APIView):
    def get(self, request, key):
        author = request.GET.get('author')
        if author:
            return Response({"message" : f"List of books by {author}"}, status=status.HTTP_200_OK)
        return Response({"message" : "List of my Books!"}, status=status.HTTP_200_OK)
    def post(self, request):
        return Response({"message" : f"Book name posted: {request.data.get('name')}"})

class MenuItemsView(generics.ListCreateAPIView):
    queryset=MenuItems.objects.all()
    serializer_class = MenuItemSerializer
class SingleMenuItem(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset=MenuItems.objects.all()
    serializer_class = MenuItemSerializer

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def display_menu(request):
    items = MenuItems.objects.all()
    if request.GET.get('category'):
        items = items.filter(category__title= request.GET.get('category'))
    perpage = request.GET.get('per_page', default=2)
    page = request.GET.get('page', default=1)
    paginator = Paginator(items, per_page=perpage)
    try:
        items= paginator.page(number=page)
    except:
        items = []
    serialized_item = MenuItemSerializer(items, many=True)
    return Response(serialized_item.data)
@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def display_single_menu(request, key):
    item = MenuItems.objects.get(id__exact=key)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)
@api_view(['POST'])
def create_single_menu(request):
    serialized_item = MenuItemSerializer(data=request.data)
    if serialized_item.is_valid(raise_exception=True):
        serialized_item.save()
        return Response({"message" : "Resource created successfully"})
    return Response({"message" : "Error occurred while creating resources!"})