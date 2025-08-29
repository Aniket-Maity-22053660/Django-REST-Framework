from rest_framework import serializers
from .models import MenuItems, Category
from decimal import Decimal

class CategorySerializer(serializers.Serializer):
    slug=serializers.SlugField()
    title= serializers.CharField(max_length=255)

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    category= serializers.SlugRelatedField(
        slug_field= 'title',
        queryset=Category.objects.all()
    )
    
    class Meta:
        model = MenuItems
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category']
    def calculate_tax(self, product:MenuItems):
        return product.price*Decimal(1.1)

