from django.shortcuts import render
from rest_framework import generics
from .models import Category,Product
from .serializers import CategorySerializer,ProductSerializer
from .permissions import IsAdminOrReadOnly

# Create your views here.

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

