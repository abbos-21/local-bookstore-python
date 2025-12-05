from django.contrib import admin
from .models import Author, Category, Book, Customer, Order, OrderItem, Review

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title","author","category","price","stock","created_at")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("category","author")

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user","phone")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","customer","created_at","status")
    inlines = [OrderItemInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book","customer","rating","created_at")
