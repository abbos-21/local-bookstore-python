from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('book/add/', views.BookCreateView.as_view(), name='book_add'),
    path('book/<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/<slug:slug>/edit/', views.BookUpdateView.as_view(), name='book_edit'),
    path('book/<slug:slug>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('book/<slug:book_slug>/add_review/', views.add_review, name='add_review'),

    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('author/add/', views.AuthorCreateView.as_view(), name='author_add'),
    path('author/<int:pk>/edit/', views.AuthorUpdateView.as_view(), name='author_edit'),
    path('author/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author_delete'),
    path("authors/<slug:slug>/", views.AuthorDetailView.as_view(), name="author_detail"),

    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('category/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path("categories/<slug:slug>/", views.CategoryDetailView.as_view(), name="category_detail"),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),

    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:book_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:book_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),

    path("my-orders/", views.MyOrdersView.as_view(), name="my_orders"),
]
