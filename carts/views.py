from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Cart, CartItem,Order,OrderItem
from .serializers import CartSerializer, CartItemSerializer,OrderSerializer,OrderItemSerializer,OrderStatusSerializer
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status




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




class CheckoutView(generics.APIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()

        if cart is None:
            return Response({'error': 'Korzina ne naydena'},status=400)

        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response({'error': 'Korzina pusta'},status=400)

        with transaction.atomic():

            for item in cart_items:
                if item.quantity > item.product.quantity:
                    return Response({'error': f'Ne xvataet tovara {item.product.name}'},status=400)

            total_price = 0

            for item in cart_items:
                total_price += item.product.price * item.quantity

            order = Order.objects.create(
                user=request.user,
                total_price=total_price
            )

            for item in cart_items:
                OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity,price=item.product.price)

            for item in cart_items:
                product = item.product
                product.quantity -= item.quantity
                product.save()

            cart_items.delete()

        return Response(OrderSerializer(order).data,status=201)



class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer
    permission_classes = [permissions.IsAdminUser]



class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)



class OrderCancelView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        with transaction.atomic():
            order = Order.objects.filter(id=pk,user=request.user).first()

            if order is None:
                return Response({'error': 'Order not found'},status=404)

            if order.status != 'pending':
                return Response({'error': 'Only pending orders can be cancelled'},status=400)

            order_items = OrderItem.objects.filter(order=order)

            for item in order_items:
                product = item.product
                product.quantity += item.quantity
                product.save()

            order.status = 'cancelled'
            order.save()

        return Response(OrderSerializer(order).data,status=200)









