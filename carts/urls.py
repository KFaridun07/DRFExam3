from django.urls import path
from .views import *

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('items/', CartItemCreateView.as_view()),
    path('items/<int:pk>/',CartItemDeleteView.as_view()),
    path('checkout/', CheckoutView.as_view()),
    path('orders/<int:pk>/status/',OrderStatusUpdateView.as_view()),
    path('orders/', OrderHistoryView.as_view()),
    path('orders/<int:pk>/', OrderDetailView.as_view()),
    path('orders/<int:pk>/cancel/',OrderCancelView.as_view()),



]