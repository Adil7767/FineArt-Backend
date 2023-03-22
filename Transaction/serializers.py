from rest_framework import serializers
from .models import *


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['add_type']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['new_category', 'icons', 'color']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['icons', 'payment_method']


class TransactionSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.add_type', read_only=True)
    payment_method_name = serializers.CharField(source='payment_method.payment_method', read_only=True)
    category_name = serializers.CharField(source='category.new_category', read_only=True)

    class Meta:
        model = Add_Transaction
        fields = ['id', 'type', 'type_name', 'payment_method', 'payment_method_name',
                  'description', 'category', 'category_name', 'amount', 'image', 'frequency']


class TotalTransactionSerializer(serializers.Serializer):
    trans_type = serializers.CharField(max_length=255)

    class Meta:
        fields = ['trans_type']