from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent']


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'slug', 'description', 'price', 'stock', 'image']


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'stock', 'image', 'category_name']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'slug', 'description',
                   'price', 'stock', 'image', 'created_at', 'updated_at']