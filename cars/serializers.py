from rest_framework import serializers
from .models import Car, CarImage, Brand, Category, Dealer, Customer


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = "__all__"


class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):

    user = serializers.CharField(
        source="user.username",
        read_only=True
    )

    purchased_car = serializers.CharField(
        source="purchased_car.model",
        read_only=True
    )

    class Meta:
        model = Customer
        fields = "__all__"