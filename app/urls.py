from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cars.api import (
    CarViewSet,
    BrandViewSet,
    CategoryViewSet,
    DealerViewSet,
    CustomerViewSet,
    CarImageViewSet,
    UserProfileViewSet
)

router = DefaultRouter()

router.register(
    r"cars",
    CarViewSet,
    basename="cars"
)

router.register(
    r"brands",
    BrandViewSet,
    basename="brands"
)

router.register(
    r"categories",
    CategoryViewSet,
    basename="categories"
)

router.register(
    r"dealers",
    DealerViewSet,
    basename="dealers"
)

router.register(
    r"customers",
    CustomerViewSet,
    basename="customers"
)

router.register(
    r"car-images",
    CarImageViewSet,
    basename="car-images"
)

router.register(
    r"userprofile",
    UserProfileViewSet,
    basename="userprofile"
)

urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "api/",
        include(router.urls)
    ),

] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)