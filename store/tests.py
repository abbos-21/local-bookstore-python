from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Author, Category, Book, Customer, Order, OrderItem

class ModelTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Author A")
        self.cat = Category.objects.create(name="Cat A", slug="cat-a")
        self.book = Book.objects.create(title="Test Book", slug="test-book", author=self.author, category=self.cat, price=9.99, stock=10)
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.customer = Customer.objects.create(user=self.user)

    def test_book_str(self):
        self.assertEqual(str(self.book), "Test Book")

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(name="Author A")
        self.cat = Category.objects.create(name="Cat A", slug="cat-a")
        self.book = Book.objects.create(title="Test Book", slug="test-book", author=self.author, category=self.cat, price=9.99, stock=10)

    def test_book_list_view(self):
        resp = self.client.get(reverse('store:book_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Test Book")

class ApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(name="Author A")
        self.cat = Category.objects.create(name="Cat A", slug="cat-a")
        self.book = Book.objects.create(title="Test Book", slug="test-book", author=self.author, category=self.cat, price=9.99, stock=10)

    def test_api_books_list(self):
        resp = self.client.get('/api/books/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Test Book', str(resp.content))
