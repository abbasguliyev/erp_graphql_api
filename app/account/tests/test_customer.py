from django.test import TestCase
from account.models import (
    Customer,
    Region
)
from django.contrib.auth import get_user_model

class CustomerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="admin", password="Admin123!")
        self.user.save()
        self.region = Region(region_name="Baku")
        self.region.save()
        self.customer = Customer(
            first_name="Name",
            last_name="Surname",
            father_name="FatherName",
            phone_number_1="123456",
            email="test@gmail.com",
            address="Test",
            region=self.region,
            note="Test Note",
            executor=self.user,
            order_count=0
        )
        self.customer.save()

    def tearDown(self) -> None:
        self.user.delete()
        self.customer.delete()
        self.region.delete()

    def test_read_customer(self):
        self.assertEqual(self.customer.first_name, "Name")
        self.assertEqual(self.customer.last_name, "Surname")
        self.assertEqual(self.customer.father_name, "FatherName")
        self.assertEqual(self.customer.phone_number_1, "123456")
        self.assertEqual(self.customer.email, "test@gmail.com")
        self.assertEqual(self.customer.address, "Test")
        self.assertEqual(self.customer.region, self.region)
        self.assertEqual(self.customer.note, "Test Note")
        self.assertEqual(self.customer.executor, self.user)
        self.assertEqual(self.customer.is_active, True)
        self.assertEqual(self.customer.fullname, "Name Surname FatherName")

    def test_customer_is_active(self):
        self.assertEqual(self.customer.is_active, True)

    def test_update_customer_is_active(self):
        self.customer.is_active = False
        self.assertEqual(self.customer.is_active, False)

    def test_customer_default_order_count(self):
        self.assertEqual(self.customer.order_count, 0)

    def test_customer_default_customer_type(self):
        self.assertEqual(self.customer.customer_type, "Standart")

    # def test_customer_increase_order_count_with_argument(self):
    #     self.customer.increase_order_count(quantity=5)
    #     self.assertEqual(self.customer.order_count, 5)

    # def test_customer_increase_order_count_without_argument(self):
    #     self.customer.increase_order_count()
    #     self.assertEqual(self.customer.order_count, 1)
