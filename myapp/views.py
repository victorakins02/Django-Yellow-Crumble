import logging

from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

# NEW

from django.shortcuts import render , HttpResponse
from .models import Career, Category, MenuItem

def home(request):
    return render(request , 'home.html')

def index(request):
    categories = Category.objects.all().prefetch_related('menuitem_set')
    return render(request, 'index.html', {'categories': categories})

def login(request):
    return render(request, 'login.html')

def about(request):
    return render(request , 'about.html')

def contact(request):
    return render(request , 'contact.html')

def faq(request):
    return render(request , 'faq.html')

def careers(request):
    careers = Career.objects.all()
    return render(request , 'careers.html', {"careers": careers})

def gallery(request):
    return render(request , 'gallery.html')

