from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache

from .models import Category, Product
from .serializer import CategorySerializer, ProductListSerializer, ProductDetailSerializer,ProductCreateUpdateSerializer
from .filters import ProductFilter

from interactions.models import Like, Comment
from interactions.serializer import CommentSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()] 
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        # 1. Redis keshidan qidirib ko'ramiz
        cached_data = cache.get('product_list')
        if cached_data is not None:
            return Response(cached_data)

        # 2. Agar keshda bo'lmasa, odatdagidek ishlaydi
        response = super().list(request, *args, **kwargs)

        # 3. Olingan natijani Redis keshiga yozib qo'yamiz (15 daqiqaga)
        cache.set('product_list', response.data, timeout=60 * 15)
        return response
    

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        product = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, product=product)
        if not created:
            like.delete()
            return Response({'liked': False})
        return Response({'liked': True}, status=201)

    @action(detail=True, methods=['get', 'post'], permission_classes=[AllowAny], url_path='comments')
    def comments(self, request, pk=None):
        product = self.get_object()

        if request.method == 'GET':
            qs = product.comments.select_related('user').all()
            return Response(CommentSerializer(qs, many=True).data)


        if not request.user.is_authenticated:
            return Response({'detail': 'Sharh qoldirish uchun tizimga kiring.'}, status=401)

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, product=product)
        return Response(serializer.data, status=201)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # 1. Redis orqali shu mahsulotning ko'rishlar sonini 1 taga oshiramiz
        view_key = f"product_views_{instance.id}"
        views_count = cache.get(view_key, 0)
        views_count += 1
        cache.set(view_key, views_count)

        # 2. Odatdagi serializer ma'lumotini olamiz
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        # 3. Ko'rishlar sonini javobga qo'shib yuboramiz
        data['views_count'] = views_count
        
        return Response(data)