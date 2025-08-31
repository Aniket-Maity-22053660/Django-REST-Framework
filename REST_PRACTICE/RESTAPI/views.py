from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import MenuItemSerializer
from .models import MenuItems, Category
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes, throttle_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from RESTAPI.forms import DemoForm, ModelForm
from django.http import HttpResponse, HttpResponseNotFound
from datetime import datetime
from django import forms
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
    if request.method == 'GET':
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
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def display_form(request):
    demoForm = DemoForm()
    if request.method == 'POST':
        demoForm = DemoForm(request.POST)
        if demoForm.is_valid():
            Category.objects.create(
                slug=demoForm.cleaned_data["slug"],
                title=demoForm.cleaned_data["title"]
            )
            return HttpResponse("Resource submitted successfully!")
    context = {'form' : demoForm}
    return render(request, 'form.html', context)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def display_menu_form(request):
    modelForm = ModelForm()
    if request.method == 'POST':
        modelForm = ModelForm(request.POST)
        if modelForm.is_valid():
            modelForm.save()
            return HttpResponse('Form submitted successfully!')
    context = {'model_form' : modelForm}
    return render(request, 'menu.html', context)

@api_view()
@permission_classes([AllowAny])
def my_view(request):
    p = MenuItems.objects.all()
    serialized_item = MenuItemSerializer(p, many=True)
    context = {'menu' : serialized_item.data, 'current' : datetime.now()}

    return render(request, 'detail.html', context)


