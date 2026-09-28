from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'price', 'count', 'subtotal']
        read_only_fields = ['id']

    def get_subtotal(self, obj):
        if obj.product:
            return obj.product.price * obj.count
        return 0


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum(
            item.product.price * item.count
            for item in obj.items.select_related('product').all()
            if item.product
        )


class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Bunday mahsulot topilmadi")
        return value


class CartRemoveSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()



class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'count', 'price_at_purchase', 'price']
        read_only_fields = ['id', 'price_at_purchase', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'address', 'status', 'items', 'total_price', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']


    def get_total_price(self, obj):
        return obj.total_price  


class CheckoutSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=120)