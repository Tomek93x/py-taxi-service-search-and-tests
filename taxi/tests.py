from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Driver, Car, Manufacturer


class DriverListSearchTest(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.login(username="testuser", password="testpass")
        self.driver1 = Driver.objects.create(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create(
            username="alice",
            first_name="Alice",
            last_name="Smith",
            license_number="XYZ98765"
        )

    def test_search_driver_by_username(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(f"{url}?q=john")
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "alice")

    def test_search_driver_case_insensitive(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(f"{url}?q=JOHN")
        self.assertContains(response, "john_doe")

    def test_search_driver_no_results(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(f"{url}?q=notfound")
        self.assertNotContains(response, "john_doe")
        self.assertNotContains(response, "alice")
        self.assertContains(response, "No drivers found")


class CarListSearchTest(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.login(username="testuser", password="testpass")
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(model="Corolla", manufacturer=self.manufacturer)
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)

    def test_search_car_by_model(self):
        url = reverse("taxi:car-list")
        response = self.client.get(f"{url}?q=Corolla")
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Camry")

    def test_search_car_no_results(self):
        url = reverse("taxi:car-list")
        response = self.client.get(f"{url}?q=Tesla")
        self.assertContains(response, "No cars found")


class ManufacturerListSearchTest(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.login(username="testuser", password="testpass")
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Audi", country="Germany")

    def test_search_manufacturer_by_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(f"{url}?q=Ford")
        self.assertContains(response, "Ford")
        self.assertNotContains(response, "Audi")

    def test_search_manufacturer_case_insensitive(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(f"{url}?q=ford")
        self.assertContains(response, "Ford")

    def test_search_manufacturer_no_results(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(f"{url}?q=Fiat")
        self.assertContains(response, "No manufacturers found")
