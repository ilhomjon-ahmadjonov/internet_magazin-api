from django.urls import path
from .views import LikeListView

urlpatterns = [
    path('likes/', LikeListView.as_view()),
]