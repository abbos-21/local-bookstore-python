# store/api_urls.py
from django.urls import path
from . import api_views

urlpatterns = [
    path('books/', api_views.BookListCreateAPI.as_view(), name='api_books'),
    path('books/<int:pk>/', api_views.BookRetrieveUpdateDestroyAPI.as_view(), name='api_book_detail'),

    path('authors/', api_views.AuthorListCreateAPI.as_view(), name='api_authors'),
    path('authors/<int:pk>/', api_views.AuthorRetrieveUpdateDestroyAPI.as_view(), name='api_author_detail'),
    
    path('categories/', api_views.CategoryListCreateAPI.as_view(), name='api_categories'),
    path('categories/<int:pk>/', api_views.CategoryRetrieveUpdateDestroyAPI.as_view(), name='api_category_detail'),
    
    path('reviews/', api_views.ReviewListCreateAPI.as_view(), name='api_reviews'),
    path('reviews/<int:pk>/', api_views.ReviewRetrieveUpdateDestroyAPI.as_view(), name='api_review_detail'),
    
    path('orders/', api_views.OrderListCreateAPI.as_view(), name='api_orders'),
    path('orders/<int:pk>/', api_views.OrderRetrieveUpdateDestroyAPI.as_view(), name='api_order_detail'),
]
