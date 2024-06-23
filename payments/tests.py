from django.test import TestCase
from django.urls import reverse
from .models import Transaction
from .forms import TransactionForm

class PaymentModelsTestCase(TestCase):
    def test_payment_model(self):
        payment = Transaction.objects.create(field1='value1', field2='value2')
        self.assertEqual(payment.field1, 'value1')

class PaymentFormsTestCase(TestCase):
    def test_payment_form(self):
        form_data = {'field1': 'value1', 'field2': 'value2'}
        form = TransactionForm(data=form_data)
        self.assertTrue(form.is_valid())

class PaymentViewsTestCase(TestCase):
    def test_payment_view(self):
        response = self.client.get(reverse('payment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payments/payment.html')