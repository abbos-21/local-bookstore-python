from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Book, Author, Category, Review, Customer, Order, OrderItem
from .forms import RegisterForm, BookForm, AuthorForm, CategoryForm, ReviewForm, CustomerForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction

class MyOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "store/my_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return Order.objects.filter(customer=customer).order_by("-created_at")


class BookListView(ListView):
    model = Book
    template_name = 'store/book_list.html'
    context_object_name = 'books'
    paginate_by = 9

class BookDetailView(DetailView):
    model = Book
    template_name = 'store/book_detail.html'
    context_object_name = 'book'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['review_form'] = ReviewForm()
        return ctx

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'store/book_form.html'
    success_url = reverse_lazy('store:book_list')

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'store/book_form.html'
    success_url = reverse_lazy('store:book_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'store/book_confirm_delete.html'
    success_url = reverse_lazy('store:book_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class AuthorListView(ListView):
    model = Author
    template_name = 'store/author_list.html'
    context_object_name = 'authors'

class AuthorDetailView(DetailView):
    model = Author
    template_name = "store/author_detail.html"
    context_object_name = "author"
    slug_field = "slug"
    slug_url_kwarg = "slug"    

class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'store/author_form.html'
    success_url = reverse_lazy('store:author_list')

class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'store/author_form.html'
    success_url = reverse_lazy('store:author_list')

class AuthorDeleteView(LoginRequiredMixin, DeleteView):
    model = Author
    template_name = 'store/author_confirm_delete.html'
    success_url = reverse_lazy('store:author_list')


class CategoryListView(ListView):
    model = Category
    template_name = 'store/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = "store/category_detail.html"
    context_object_name = "category"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'store/category_form.html'
    success_url = reverse_lazy('store:category_list')

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'store/category_form.html'
    success_url = reverse_lazy('store:category_list')

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'store/category_confirm_delete.html'
    success_url = reverse_lazy('store:category_list')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # create customer
            Customer.objects.create(user=user)
            login(request, user)
            return redirect('store:book_list')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('store:book_list')
        else:
            messages.error(request, "Invalid credentials")
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('store:book_list')

@login_required
def profile_view(request):
    customer = get_object_or_404(Customer, user=request.user)
    return render(request, 'store/profile.html', {'customer': customer})

@login_required
def profile_edit_view(request):
    customer = get_object_or_404(Customer, user=request.user)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('store:profile')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'store/profile.html', {'form': form})


@login_required
def add_review(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.customer = Customer.objects.get(user=request.user)
            review.save()
            messages.success(request, "Review submitted.")
    return redirect(book.get_absolute_url())

CART_SESSION_ID = 'cart'

def _get_cart(request):
    return request.session.get(CART_SESSION_ID, {})

def _save_cart(request, cart):
    request.session[CART_SESSION_ID] = cart
    request.session.modified = True

def cart_add(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = _get_cart(request)
    item = cart.get(str(book_id), {'quantity': 0, 'price': float(book.price)})
    item['quantity'] = item.get('quantity', 0) + 1
    cart[str(book_id)] = item
    _save_cart(request, cart)
    messages.success(request, f"Added {book.title} to cart.")
    return redirect('store:book_list')

def cart_remove(request, book_id):
    cart = _get_cart(request)
    if str(book_id) in cart:
        del cart[str(book_id)]
        _save_cart(request, cart)
        messages.success(request, "Item removed from cart.")
    return redirect('store:cart')

def cart_view(request):
    cart = _get_cart(request)
    cart_items = []
    total = 0
    for book_id, item in cart.items():
        book = get_object_or_404(Book, id=int(book_id))
        subtotal = book.price * item['quantity']
        total += subtotal
        cart_items.append({'book': book, 'quantity': item['quantity'], 'subtotal': subtotal})
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
@transaction.atomic
def checkout_view(request):
    customer = get_object_or_404(Customer, user=request.user)
    cart = _get_cart(request)
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('store:book_list')

    if request.method == 'POST':
        order = Order.objects.create(customer=customer)
        for book_id, item in cart.items():
            book = get_object_or_404(Book, id=int(book_id))
            qty = int(item['quantity'])
            OrderItem.objects.create(order=order, book=book, quantity=qty)
            
            if book.stock >= qty:
                book.stock -= qty
                book.save()
        
        request.session.pop(CART_SESSION_ID, None)
        messages.success(request, f"Order #{order.id} placed.")
        return redirect('store:order_detail', pk=order.id)
    else:
        
        cart_items = []
        total = 0
        for book_id, item in cart.items():
            book = get_object_or_404(Book, id=int(book_id))
            subtotal = book.price * item['quantity']
            total += subtotal
            cart_items.append({'book': book, 'quantity': item['quantity'], 'subtotal': subtotal})
        return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total': total})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'store/order_detail.html', {'order': order})
