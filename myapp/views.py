# import necessary modules and models
from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout as a_logout

from .models import (
    Career, Category, ContactMessage, MenuItem,
    NewsletterSubscription, Order, OrderItem,
    Review, UserProfile, News
)
from .forms import UserProfileForm

# Home page view to display recent reviews and menu items
def home(request):
    # Get the 3 most recent reviews and 3 menu items to display on the home page
    reviews = Review.objects.all().order_by('-created_at')[:3]
    items = MenuItem.objects.all()[:3]
    return render(request, 'myapp/home.html', {'reviews': reviews, 'items': items})

# Index page view to display menu categories and cart items
def index(request):
    categories = Category.objects.all()
    cart_items = []
    total = 0
    
    # If the user is authenticated, get their active order and calculate the total price of the items in the cart
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, is_ordered=False).first()
        
        # If there is no active order, create a new one for the user
        if not order:
            order = Order.objects.create(user=request.user, is_ordered=False)
        
        # Get the items in the cart and calculate the total price
        cart_items = order.items.all()
        total = sum(item.product.price for item in cart_items)

    return render(request, 'myapp/index.html', {
        'categories': categories,
        'cart_items': cart_items,
        'total': total
    })

# Add to cart view to handle adding items to the cart and reducing stock
def add_to_cart(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        
        # Use a transaction to ensure that stock reduction and cart addition happen atomically
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

# Remove from cart view to handle removing items from the cart and increasing stock   
def remove_from_cart(request, item_id):
    if request.method == "POST":
        item = OrderItem.objects.get(id=item_id)
        item.delete()
        
        return redirect('index')

# Login page view to display login form
def login(request):
    return render(request, 'myapp/login.html')

# About page view to display company information and news items
def about(request):
    return render(request , 'myapp/about.html')

# FAQ page view to display frequently asked questions
def faq(request):
    return render(request , 'myapp/faq.html')

# Careers page view to display job listings 
def careers(request):
    careers = Career.objects.all()
    return render(request , 'myapp/careers.html', {"careers": careers})

# Gallery page view to display images of food and restaurant
def gallery(request):
    return render(request , 'myapp/gallery.html')

# Contact page view to handle contact form submissions and save messages to the database
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

# Reviews page view to display customer reviews and handle new review submissions
def review(request):
    if request.method == 'POST':
        Review.objects.create(
            user=request.user if request.user.is_authenticated else None,
            customer_name=request.POST.get('customer_name'),
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment')
        )
        return redirect('review')
    
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'myapp/reviews.html', {'reviews': reviews})

# Edit review view to allow users to edit their reviews
def edit_review(request, review_id):
    review = Review.objects.get(id=review_id)

    # Only allow the review author or staff to edit the review
    if not (request.user == review.user or request.user.is_staff):
        return redirect('review')

    # If the form is submitted, update the review with the new data and save it to the database
    if request.method == 'POST':
        review.customer_name = request.POST.get('customer_name')
        review.rating = request.POST.get('rating')
        review.comment = request.POST.get('comment')
        
        review.save()
        return redirect('review')

    return render(request, 'myapp/edit_review.html', {'review': review})

# Delete review view to allow users to delete their reviews
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    # Only allow the review author or staff to delete the review
    if request.user == review.user or request.user.is_staff:
        if request.method == 'POST':
            review.delete()
    
    return redirect('review')

# Newsletter subscription view to handle newsletter form submissions and save subscribers to the database
def newsletter(request):
    if request.method == 'POST':
        name = request.POST.get('name', '') 
        email = request.POST.get('email')

        # Check if the email is already subscribed to prevent duplicates
        if NewsletterSubscription.objects.filter(email=email).exists():
            return render(request, 'myapp/newsletter.html', {
                'error': 'This email is already subscribed!',
                'name': name 
            })
        NewsletterSubscription.objects.create(name=name, email=email)
        print(f"New newsletter subscription: {email}")
        
        return redirect('home')
        
    return render(request, 'myapp/newsletter.html')

# Registration view to handle user registration and create user profiles
def register(request):
    if request.method == 'POST':
        # Create a new user using the UserCreationForm and create a corresponding UserProfile
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            auth_login(request, user)
            return redirect('index') 
            
    else:
        form = UserCreationForm()
        
    return render(request, 'myapp/register.html', {'form': form})

# Login view to handle user authentication and login
def login_view(request):
    if request.method == 'POST':
        # Get the username and password from the submitted form
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user using Django's built-in authentication system
        user = authenticate(request, username=username, password=password)
        
        # If the user is authenticated successfully, log them in and redirect to the home page        
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        # Otherwise, re-render the login page with an error message
        else:
            return render(request, 'myapp/login.html', {
                'error': "Invalid username or password.",
                'form': AuthenticationForm() 
            })
    
    return render(request, 'myapp/login.html', {'form': AuthenticationForm()})

# Logout view to handle user logout
def logout_view(request):
    # Log out the user and redirect to the home page
    a_logout(request)
    return redirect('home')

def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Handle profile update form submission
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile.address = form.cleaned_data.get('address')
            profile.telephone_number = form.cleaned_data.get('telephone_number')
            profile.favorite_dessert = form.cleaned_data.get('favorite_dessert')
            profile.save()
            return redirect('profile')
    # Pre-fill the form with existing profile data when the page is loaded
    else:
        form = UserProfileForm(initial={
            'address': profile.address,
            'telephone_number': profile.telephone_number,
            'favorite_dessert': profile.favorite_dessert,
        })

    return render(request, 'myapp/profile.html', {'form': form})

# About page view to display company information and news items
def about(request):
    news_items = News.objects.all().order_by('-date_posted')
    return render(request, 'myapp/about.html', {'news_items': news_items})

# Submit order view to handle order submission, calculate total, and save order details to the database
def submit_order(request):
    if not request.user.is_authenticated:
        return redirect('login') 

    if request.method == "POST":
        name = request.POST.get('full_name')
        addr = request.POST.get('address')
        phone = request.POST.get('phone')
        
        order = Order.objects.filter(user=request.user, is_ordered=False).first()
        
        # If no active order or no items in the order, redirect to index
        if not order or not order.items.exists():
            return redirect('index')

        # Calculate total and create order summary
        cart_items = order.items.all()
        total = sum(item.product.price for item in cart_items)
        summary = ", ".join([item.product.name for item in cart_items])

        order.full_name = name
        order.address = addr
        order.phone_number = phone
        order.total_amount = total
        order.items_summary = summary
        order.is_ordered = True  
        order.save()

        # Clear the cart by deleting the order items
        categories = Category.objects.all()
        return render(request, 'myapp/index.html', {
            'categories': categories,
            'order_success': True,
            'cart_items': [],
            'total': 0
        })
    
    return redirect('index')