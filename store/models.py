from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=300, unique=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('store:book_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Order #{self.pk} - {self.customer}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.book.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.book.title}"

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} - {self.rating}"
