from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Driver, Car, Manufacturer


class DriverListSearchTest(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            username="testuser", password="testpass"
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
        self.assertIn(self.driver1, response.context["driver_list"])
        self.assertNotIn(self.driver2, response.context["driver_list"])

    def test_search_driver_case_insensitive(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(f"{url}?q=JOHN")
        self.assertIn(self.driver1, response.context["driver_list"])

    def test_search_driver_no_results(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(f"{url}?q=notfound")
        self.assertEqual(list(response.context["driver_list"]), [])


class CarListSearchTest(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car1 = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer
        )

    def test_search_car_by_model(self):
        url = reverse("taxi:car-list")
        response = self.client.get(f"{url}?q=Corolla")
        self.assertIn(self.car1, response.context["car_list"])
        self.assertNotIn(self.car2, response.context["car_list"])

    def test_search_car_case_insensitive(self):
        url = reverse("taxi:car-list")
        resp_low = self.client.get(f"{url}?q=corolla")
        resp_up = self.client.get(f"{url}?q=COROLLA")
        self.assertIn(self.car1, resp_low.context["car_list"])
        self.assertIn(self.car1, resp_up.context["car_list"])

    def test_search_car_no_results(self):
        url = reverse("taxi:car-list")
        response = self.client.get(f"{url}?q=Tesla")
        self.assertEqual(list(response.context["car_list"]), [])


class ManufacturerListSearchTest(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")
        self.man1 = Manufacturer.objects.create(name="Ford", country="USA")
        self.man2 = Manufacturer.objects.create(name="Audi", country="Germany")

    def test_search_manufacturer_by_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(f"{url}?q=Ford")
        self.assertIn(self.man1, response.context["manufacturer_list"])
        self.assertNotIn(self.man2, response.context["manufacturer_list"])

    def test_search_manufacturer_case_insensitive(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(f"{url}?q=ford")
        self.assertIn(self.man1, response.context["manufacturer_list"])

    def test_search_manufacturer_no_results(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(f"{url}?q=Fiat")
        self.assertEqual(list(response.context["manufacturer_list"]), [])
