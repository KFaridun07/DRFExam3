from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer



class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart = Cart.objects.filter(user=self.request.user).first()

        if cart is None:
            cart = Cart.objects.create(user=self.request.user)

        return cart



class CartItemCreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart = Cart.objects.filter(user=self.request.user).first()

        if cart is None:
            cart = Cart.objects.create(user=self.request.user)

        serializer.save(cart=cart)



class CartItemDeleteView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart = Cart.objects.filter(user=self.request.user).first()

        if cart is None:
            return CartItem.objects.none()

        return CartItem.objects.filter(cart=cart)



