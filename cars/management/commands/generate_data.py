from django.core.management.base import BaseCommand
from faker import Faker
from cars.models import Car, Brand, Category, Dealer
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()

        brands = [
            Brand.objects.create(name="Toyota"),
            Brand.objects.create(name="Honda"),
            Brand.objects.create(name="BMW"),
        ]

        categories = [
            Category.objects.create(name="Sedan"),
            Category.objects.create(name="Coupe"),
            Category.objects.create(name="SUV"),
        ]

        dealers = [
            Dealer.objects.create(name="AutoWorld", city="City A"),
            Dealer.objects.create(name="FastDrive", city="City B"),
        ]

        for _ in range(1000):
            Car.objects.create(
                model=fake.word(),
                year=int(fake.year()),
                brand=random.choice(brands),
                category=random.choice(categories),
                dealer=random.choice(dealers),
            )