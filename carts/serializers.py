
from rest_framework import serializers
from .models import Cart, CartItem,Order,OrderItem
from products.models import Product
from products.serializers import ProductSerializer



class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'product', 'quantity']
        read_only_fields = ['id']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('Kolichestvo doljen bit polojitelnim')

        return value


    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity')

        if product and quantity:
            cart = self.context['request'].user.cart

            cart_item = CartItem.objects.filter(cart=cart,product=product).first()

            current_quantity = 0

            if cart_item:
                current_quantity = cart_item.quantity

            if current_quantity + quantity > product.quantity:
                raise serializers.ValidationError(
                    'Not enough products in stock'
                )

        return data



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']
        read_only_fields = ['id', 'user', 'created_at']



class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id','product','product_name','quantity','price',]
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id','total_price','status','created_at','items',]
        read_only_fields = fields


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        if value not in ['pending', 'processed', 'cancelled']:
            raise serializers.ValidationError('Invalid order status')
        return value


