import logging

from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone


# NEW

from django.shortcuts import render , HttpResponse
from django.db import transaction
from .models import UserProfile
from .forms import UserProfileForm

from myapp.forms import ContactForm, ReviewForm
from .models import Career, Category, ContactMessage, MenuItem, NewsletterSubscription, Order, OrderItem, Review, UserProfile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout as a_logout
from .models import UserProfile

def home(request):
    reviews = Review.objects.all().order_by('-created_at')[:3]
    items = MenuItem.objects.all()[:3]
    return render(request, 'myapp/home.html', {'reviews': reviews, 'items': items})

def index(request):
    categories = Category.objects.all()
    order, created = Order.objects.get_or_create(is_ordered=False)
    cart_items = order.items.all()
    
    total = sum(item.product.price for item in cart_items)

    return render(request, 'myapp/index.html', {
        'categories': categories,
        'cart_items': cart_items,
        'total': total
    })

def add_to_cart(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        
        with transaction.atomic():
            product = MenuItem.objects.get(id=item_id)
            if product.stock > 0:
                product.stock -= 1
                product.save()
            
                order, created = Order.objects.get_or_create(is_ordered=False)
                OrderItem.objects.create(order=order, product=product)
                
                print(f"Success: {product.name} added and stock reduced to {product.stock}")
            else:
                print("Error: Out of stock!")

        return redirect('index')
    
def remove_from_cart(request, item_id):
    if request.method == "POST":
        item = OrderItem.objects.get(id=item_id)
        item.delete()
        
        return redirect('index')

def login(request):
    return render(request, 'myapp/login.html')

def about(request):
    return render(request , 'myapp/about.html')

def faq(request):
    return render(request , 'myapp/faq.html')

def careers(request):
    careers = Career.objects.all()
    return render(request , 'myapp/careers.html', {"careers": careers})

def gallery(request):
    return render(request , 'myapp/gallery.html')

def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            first_name=request.POST.get('firstName'),
            last_name=request.POST.get('lastName'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )
        return redirect('home') 
    
    return render(request, 'myapp/contact.html')

def review(request):
    if request.method == 'POST':
        Review.objects.create(
            customer_name=request.POST.get('customer_name'),
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment')
        )
        return redirect('review')
    
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'myapp/reviews.html', {'reviews': reviews})

def edit_review(request, review_id):
    review = Review.objects.get(id=review_id)

    if request.method == 'POST':
        review.customer_name = request.POST.get('customer_name')
        review.rating = request.POST.get('rating')
        review.comment = request.POST.get('comment')
        
        review.save()
        return redirect('review')

    return render(request, 'myapp/edit_review.html', {'review': review})

def delete_review(request, review_id):
    if request.method == 'POST':
        try:
            review = Review.objects.get(id=review_id)
            review.delete()
            print(f"Review {review_id} deleted successfully!")
        except Review.DoesNotExist:
            print(f"Review {review_id} was not found, skipping delete.")
            
    return redirect('review')

def newsletter(request):
    if request.method == 'POST':
        name = request.POST.get('name', '') 
        email = request.POST.get('email')
    
        NewsletterSubscription.objects.create(name=name, email=email)
        
        print(f"New newsletter subscription: {email}")
        return redirect('home')
        
    return render(request, 'myapp/newsletter.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            auth_login(request, user)
            return redirect('index') 
            
    else:
        form = UserCreationForm()
        
    return render(request, 'myapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'myapp/login.html', {
                'error': "Invalid username or password.",
                'form': AuthenticationForm() 
            })
    
    return render(request, 'myapp/login.html', {'form': AuthenticationForm()})

def logout_view(request):
    a_logout(request)
    return redirect('home')

def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile.address = form.cleaned_data.get('address')
            profile.telephone_number = form.cleaned_data.get('telephone_number')
            profile.favorite_dessert = form.cleaned_data.get('favorite_dessert')
            profile.save()
            return redirect('profile')
    else:
        form = UserProfileForm(initial={
            'address': profile.address,
            'telephone_number': profile.telephone_number,
            'favorite_dessert': profile.favorite_dessert,
        })

    return render(request, 'myapp/profile.html', {'form': form})