import logging

from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

# NEW

from django.shortcuts import render , HttpResponse
from .models import Career, Category, MenuItem

def home(request):
    return render(request , 'myapp/home.html')

def index(request):
    categories = Category.objects.all().prefetch_related('menuitem_set')
    return render(request, 'myapp/index.html', {'categories': categories})

def login(request):
    return render(request, 'myapp/login.html')

def about(request):
    return render(request , 'myapp/about.html')

def contact(request):
    return render(request , 'myapp/contact.html')

def faq(request):
    return render(request , 'myapp/faq.html')

def careers(request):
    careers = Career.objects.all()
    return render(request , 'myapp/careers.html', {"careers": careers})

def gallery(request):
    return render(request , 'myapp/gallery.html')

