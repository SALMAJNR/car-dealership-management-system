from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg, Count, Max, Min
from django.http import HttpResponse

from openpyxl import Workbook

from cars.models import Car, Brand, Category, Dealer, Customer, CarImage

from cars.serializers import (
    CarSerializer,
    BrandSerializer,
    CategorySerializer,
    DealerSerializer,
    CustomerSerializer,
    CarImageSerializer,
)


class StatsSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    avg = serializers.FloatField()
    max = serializers.IntegerField()
    min = serializers.IntegerField()


class UserProfileViewSet(GenericViewSet):

    @action(methods=["GET"], detail=False, url_path="my")
    def my(self, request):
        if request.user.is_authenticated:
            role = "admin" if request.user.is_superuser else "customer"

            return Response({
                "id": request.user.id,
                "username": request.user.username,
                "role": role,
            })

        return Response({}, status=401)

    @action(methods=["POST"], detail=False, url_path="login")
    def login(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password")
        )

        if user:
            login(request, user)

            role = "admin" if user.is_superuser else "customer"

            return Response({
                "success": True,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": role,
                }
            })

        return Response({
            "success": False,
            "error": "Invalid credentials"
        }, status=400)

    @action(methods=["POST"], detail=False, url_path="logout")
    def logout(self, request):
        logout(request)

        return Response({
            "success": True
        })


class CarViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Car.objects.all().order_by("-id")
    serializer_class = CarSerializer

    @action(detail=False, methods=["GET"], url_path="stats")
    def stats(self, request):
        stats = Car.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            min=Min("id"),
            max=Max("id"),
        )

        serializer = StatsSerializer(instance=stats)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], url_path="export_excel")
    def export_excel(self, request):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Cars"

        worksheet.append([
            "Model",
            "Brand",
            "Category",
            "Dealer",
            "Year"
        ])

        for car in Car.objects.all():
            worksheet.append([
                car.model,
                car.brand.name if car.brand else "",
                car.category.name if car.category else "",
                car.dealer.name if car.dealer else "",
                car.year
            ])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        response["Content-Disposition"] = 'attachment; filename="cars.xlsx"'

        workbook.save(response)

        return response


class BrandViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DealerViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer


class CustomerViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        if not self.request.user.is_authenticated:
            return qs.none()

        if self.request.user.is_superuser:
            return qs

        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["POST"], url_path="bind-car")
    def bind_car(self, request):
        car_id = request.data.get("car_id")

        Customer.objects.create(
            user=request.user,
            purchased_car_id=car_id
        )

        return Response({
            "success": True
        })


class CarImageViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer

    @action(detail=False, methods=["GET"], url_path="stats")
    def stats(self, request):
        stats = CarImage.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            min=Min("id"),
            max=Max("id"),
        )

        serializer = StatsSerializer(instance=stats)
        return Response(serializer.data)