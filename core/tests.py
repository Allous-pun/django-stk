from django.test import TestCase
from django.urls import reverse
from .models import Package

class CoreModelsTestCase(TestCase):
    def test_my_model(self):
        my_model = Package.objects.create(field1='value1', field2='value2')
        self.assertEqual(my_model.field1, 'value1')

class CoreViewsTestCase(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')