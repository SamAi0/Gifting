from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product, Category

class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Test Category")
        self.product1 = Product.objects.create(
            name="Test Product 1",
            description="Description 1",
            price=100.00,
            category=self.category
        )
        self.product2 = Product.objects.create(
            name="Test Product 2",
            description="Description 2",
            price=200.00,
            category=self.category
        )
        self.url = reverse('product-list')

    def test_fetch_products_paginated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)

    def test_unique_slug_generation(self):
        # Create product with same name
        product3 = Product.objects.create(
            name="Test Product 1",
            description="Description 3",
            price=150.00,
            category=self.category
        )
        self.assertNotEqual(self.product1.slug, product3.slug)
        self.assertTrue(product3.slug.startswith('test-product-1-'))

    def test_price_validation(self):
        from django.core.exceptions import ValidationError
        product = Product(
            name="Negative Price Product",
            description="Bad Price",
            price=-10.00,
            category=self.category
        )
        with self.assertRaises(ValidationError):
            product.full_clean()
