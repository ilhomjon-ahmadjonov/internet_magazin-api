from rest_framework import serializers
from .models import Like, Comment
from products.serializer import ProductListSerializer


class LikeSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)


    class Meta:
        model = Like
        fields = ['id', 'product', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)


    class Meta:
        model = Comment
        fields = ['id', 'username', 'text', 'rating', 'created_at']
        read_only_fields = ['id', 'username', 'created_at']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Baho 1 dan 5 gacha bo'lishi kerak")
        return value