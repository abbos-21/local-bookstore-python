from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Book, Author, Category, Review, Customer

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username","email","first_name","last_name")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("Passwords don't match.")
        return cd.get('password2')

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','slug','author','category','description','price','stock','cover']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name','bio']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','slug']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','comment']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone','address']
