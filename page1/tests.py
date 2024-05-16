from django.test import TestCase
from django.utils import timezone
from page1.models import *

class TestCustomerID(TestCase):
    def test_cust_id_increment(self):
        # Create a customer with cust_id at 9999 for the current year
        current_year = timezone.now().year % 100
        last_customer = Customer.objects.create(cust_id=current_year * 10000 + 9999)

        # Save a new customer, it should increment the cust_id and add an additional zero
        new_customer = Customer()
        new_customer.save()

        # Check if the cust_id is incremented and has an additional zero
        self.assertEqual(new_customer.cust_id, current_year * 100000 + 1)
