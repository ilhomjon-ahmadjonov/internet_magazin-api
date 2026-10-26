from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status,generics
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.cache import cache

from .models import Cart, CartItem,Order, OrderItem
from .serializer import CartSerializer, CartAddSerializer, CartRemoveSerializer,OrderSerializer, CheckoutSerializer
from products.models import Product


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Redis'dan foydalanuvchi savatini o'qimiz
        cart_key = f"cart_{request.user.id}"
        cart_data = cache.get(cart_key) or {}
        return Response(cart_data)


class CartAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = str(serializer.validated_data['product_id'])
        quantity = serializer.validated_data['quantity']

        # Mahsulot bazada borligini tekshiramiz
        product = get_object_or_404(Product, id=product_id)

        cart_key = f"cart_{request.user.id}"
        cart = cache.get(cart_key) or {"items": {}}

        # Savatda bo'lsa miqdorini qo'shamiz, bo'lmasa yangidan qo'shamiz
        if product_id in cart["items"]:
            cart["items"][product_id]["quantity"] += quantity
        else:
            cart["items"][product_id] = {
                "product_id": product.id,
                "name": product.name,
                "price": str(product.price),
                "quantity": quantity
            }

        # Redis'ga saqlaymiz (masalan, 2 кун муддатга)
        cache.set(cart_key, cart, timeout=60 * 60 * 48)
        return Response(cart, status=status.HTTP_201_CREATED)


class CartRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CartRemoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = str(serializer.validated_data['product_id'])

        cart_key = f"cart_{request.user.id}"
        cart = cache.get(cart_key)

        if not cart or "items" not in cart or product_id not in cart["items"]:
            return Response({'detail': "Bu mahsulot savatda topilmadi"}, status=404)

        # Mahsulotni savatdan o'chiramiz
        del cart["items"][product_id]
        cache.set(cart_key, cart, timeout=60 * 60 * 48)

        return Response(cart, status=status.HTTP_200_OK)




class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.validated_data['address']

        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.select_related('product').all()

        if not cart_items.exists():
            return Response({'detail': "Savat bo'sh"}, status=status.HTTP_400_BAD_REQUEST)

        for item in cart_items:
            if item.product is None:
                return Response(
                    {'detail': "Savatdagi mahsulotlardan biri endi mavjud emas"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if item.product.stock < item.count:
                return Response(
                    {'detail': f"{item.product.name} omborda yetarli emas (mavjud: {item.product.stock})"},
                    status=status.HTTP_400_BAD_REQUEST
                )


        with transaction.atomic():
            order = Order.objects.create(user=request.user, address=address)

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    count=item.count,
                    price_at_purchase=item.product.price

                )
                item.product.stock -= item.count
                item.product.save()

            cart_items.delete()


        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')