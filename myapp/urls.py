from django.urls import path
from . import views 

urlpatterns = [
    path("", views.home, name="home"),
    path("index.html/", views.index, name="index"),
    path("login.html/", views.login, name="login"),
    path("about.html/", views.about, name="about"),
    path("contact.html/", views.contact, name="contact"),
    path("faq.html/", views.faq, name="faq"),
    path("careers.html/", views.careers, name="careers"),
    path("gallery.html/", views.gallery, name="gallery"),
]