from django.db import models
from django.contrib.auth.models import User


class Brand(models.Model):

    name = models.TextField()

    picture = models.ImageField(
        upload_to="brands",
        null=True,
        blank=True
    )

    def __str__(self):

        return self.name


class Category(models.Model):

    name = models.TextField()

    def __str__(self):

        return self.name


class Dealer(models.Model):

    name = models.TextField()

    city = models.TextField()

    picture = models.ImageField(
        upload_to="dealers",
        null=True,
        blank=True
    )

    def __str__(self):

        return f"{self.name} ({self.city})"


class Car(models.Model):

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    model = models.TextField()

    year = models.IntegerField()

    picture = models.ImageField(
        upload_to="cars",
        null=True,
        blank=True
    )

    def __str__(self):

        return self.model


class CarImage(models.Model):

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="cars",
        null=True,
        blank=True
    )

    def __str__(self):

        return f"Image for {self.car.model}"


class Customer(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    purchased_car = models.ForeignKey(
        Car,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):

        if self.user:
            return self.user.username

        return "No User"


class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    role = models.CharField(
        max_length=20,
        default="customer"
    )

    def __str__(self):

        return f"{self.user.username} ({self.role})"