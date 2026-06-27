from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from .models import Brand, Category, Dealer, Car, Customer


class BrandViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_brands(self):
        baker.make(Brand, 3)
        r = self.client.get("/api/brands/")
        data = r.json()
        assert r.status_code == 200
        assert len(data) == 3

    def test_create_brand(self):
        r = self.client.post("/api/brands/", {"name": "BMW"}, format="json")
        assert r.status_code == 201

    def test_retrieve_brand(self):
        brand = baker.make(Brand)
        r = self.client.get(f"/api/brands/{brand.id}/")
        data = r.json()
        assert r.status_code == 200
        assert data["id"] == brand.id

    def test_update_brand(self):
        brand = baker.make(Brand)
        r = self.client.put(
            f"/api/brands/{brand.id}/",
            {"name": "Updated"},
            format="json",
        )
        assert r.status_code == 200

    def test_delete_brand(self):
        brand = baker.make(Brand)
        r = self.client.delete(f"/api/brands/{brand.id}/")
        assert r.status_code == 204


class CategoryViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_categories(self):
        baker.make(Category, 2)
        r = self.client.get("/api/categories/")
        data = r.json()
        assert r.status_code == 200
        assert len(data) == 2

    def test_create_category(self):
        r = self.client.post("/api/categories/", {"name": "SUV"}, format="json")
        assert r.status_code == 201

    def test_retrieve_category(self):
        category = baker.make(Category)
        r = self.client.get(f"/api/categories/{category.id}/")
        data = r.json()
        assert r.status_code == 200
        assert data["id"] == category.id

    def test_update_category(self):
        category = baker.make(Category)
        r = self.client.put(
            f"/api/categories/{category.id}/",
            {"name": "Updated"},
            format="json",
        )
        assert r.status_code == 200

    def test_delete_category(self):
        category = baker.make(Category)
        r = self.client.delete(f"/api/categories/{category.id}/")
        assert r.status_code == 204


class DealerViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_dealers(self):
        baker.make(Dealer, 2)
        r = self.client.get("/api/dealers/")
        data = r.json()
        assert r.status_code == 200
        assert len(data) == 2

    def test_create_dealer(self):
        r = self.client.post(
            "/api/dealers/",
            {"name": "AutoWorld", "city": "NY"},
            format="json",
        )
        assert r.status_code == 201

    def test_retrieve_dealer(self):
        dealer = baker.make(Dealer)
        r = self.client.get(f"/api/dealers/{dealer.id}/")
        data = r.json()
        assert r.status_code == 200
        assert data["id"] == dealer.id

    def test_update_dealer(self):
        dealer = baker.make(Dealer)
        r = self.client.put(
            f"/api/dealers/{dealer.id}/",
            {"name": "Updated", "city": "LA"},
            format="json",
        )
        assert r.status_code == 200

    def test_delete_dealer(self):
        dealer = baker.make(Dealer)
        r = self.client.delete(f"/api/dealers/{dealer.id}/")
        assert r.status_code == 204


class CarViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_cars(self):
        baker.make(Car, 3)
        r = self.client.get("/api/cars/")
        data = r.json()
        assert r.status_code == 200
        assert len(data) == 3

    def test_create_car(self):
        brand = baker.make(Brand)
        category = baker.make(Category)
        dealer = baker.make(Dealer)

        r = self.client.post(
            "/api/cars/",
            {
                "brand": brand.id,
                "category": category.id,
                "dealer": dealer.id,
                "model": "X5",
                "year": 2024,
            },
            format="json",
        )
        assert r.status_code == 201

    def test_retrieve_car(self):
        car = baker.make(Car)
        r = self.client.get(f"/api/cars/{car.id}/")
        data = r.json()
        assert r.status_code == 200
        assert data["id"] == car.id

    def test_update_car(self):
        car = baker.make(Car)
        r = self.client.put(
            f"/api/cars/{car.id}/",
            {
                "brand": car.brand.id,
                "category": car.category.id,
                "dealer": car.dealer.id,
                "model": "Updated",
                "year": car.year,
            },
            format="json",
        )
        assert r.status_code == 200

    def test_delete_car(self):
        car = baker.make(Car)
        r = self.client.delete(f"/api/cars/{car.id}/")
        assert r.status_code == 204


class CustomerViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_customers(self):
        baker.make(Customer, 2)
        r = self.client.get("/api/customers/")
        data = r.json()
        assert r.status_code == 200
        assert len(data) == 2

    def test_create_customer(self):
        car = baker.make(Car)
        r = self.client.post(
            "/api/customers/",
            {"name": "John", "purchased_car": car.id},
            format="json",
        )
        assert r.status_code == 201

    def test_retrieve_customer(self):
        customer = baker.make(Customer)
        r = self.client.get(f"/api/customers/{customer.id}/")
        data = r.json()
        assert r.status_code == 200
        assert data["id"] == customer.id

    def test_update_customer(self):
        customer = baker.make(Customer)
        r = self.client.put(
            f"/api/customers/{customer.id}/",
            {"name": "Updated", "purchased_car": None},
            format="json",
        )
        assert r.status_code == 200

    def test_delete_customer(self):
        customer = baker.make(Customer)
        r = self.client.delete(f"/api/customers/{customer.id}/")
        assert r.status_code == 204