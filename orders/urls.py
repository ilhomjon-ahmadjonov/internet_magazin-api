from django.urls import path
from .views import CartView, CartAddView, CartRemoveView,CheckoutView, OrderListView


urlpatterns = [
    path('cart/', CartView.as_view()),
    path('cart/add/', CartAddView.as_view()),
    path('cart/remove/', CartRemoveView.as_view()),
    path('orders/checkout/', CheckoutView.as_view()),
    path('orders/', OrderListView.as_view()),
]