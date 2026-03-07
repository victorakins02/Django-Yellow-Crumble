import logging

from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

# NEW

from django.shortcuts import render , HttpResponse

from myapp.forms import ContactForm
from .models import Career, Category, ContactMessage, MenuItem

def home(request):
    return render(request , 'myapp/home.html')

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

