from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Like
from .serializer import LikeSerializer


class LikeListView(generics.ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user).select_related('product')