import logging

from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

# NEW

from django.shortcuts import render , HttpResponse

from myapp.forms import ContactForm, ReviewForm
from .models import Career, Category, ContactMessage, MenuItem, NewsletterSubscription, Review

def home(request):
    reviews = Review.objects.all().order_by('-created_at')[:3]
    items = MenuItem.objects.all()[:3]
    return render(request, 'myapp/home.html', {'reviews': reviews, 'items': items})

def index(request):
    categories = Category.objects.all().prefetch_related('menuitem_set')
    return render(request, 'myapp/index.html', {'categories': categories})

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
        # Create (A)
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