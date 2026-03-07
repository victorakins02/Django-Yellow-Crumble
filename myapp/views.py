import logging

from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

# NEW

from django.shortcuts import render , HttpResponse

from myapp.forms import ContactForm, ReviewForm
from .models import Career, Category, ContactMessage, MenuItem, Review

def home(request):
    reviews = Review.objects.all().order_by('-created_at')[:3]
    return render(request, 'myapp/home.html', {'reviews': reviews})

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
        # Update the fields manually
        review.customer_name = request.POST.get('customer_name')
        review.rating = request.POST.get('rating')
        review.comment = request.POST.get('comment')
        
        review.save()
        return redirect('review')

    return render(request, 'myapp/edit_review.html', {'review': review})

def delete_review(request, review_id):
    if request.method == 'POST':
        try:
            # We use .get() manually instead of get_object_or_404
            review = Review.objects.get(id=review_id)
            review.delete()
            print(f"Review {review_id} deleted successfully!")
        except Review.DoesNotExist:
            # If the review is already gone, just ignore the error
            print(f"Review {review_id} was not found, skipping delete.")
            
    # Always redirect back to the review page name from your urls.py
    return redirect('review')

