from django.urls import path
from .views import *

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('items/', CartItemCreateView.as_view()),
    path('items/<int:pk>/',CartItemDeleteView.as_view()),

]