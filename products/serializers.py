from rest_framework import serializers
from .models import Category, Product
from rest_framework.serializers import ModelSerializer


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    category = CategorySerializer(read_only = True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        source = 'category',
        write_only = True
    )
    class Meta:
        model = Product
        fields = ['id','name','description','price','quantity','category','created_at']

    def validate_price(self,value):
        if value < 0:
            raise serializers.ValidationError('Sena doljen bit polojitelnim')
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError('KOlichestvo doljen bit polojitelnim')
        return value