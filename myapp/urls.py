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
    path("reviews.html/", views.review, name="review"), 
    path("edit-review/<int:review_id>/", views.edit_review, name="edit_review"),
    path("delete-review/<int:review_id>/", views.delete_review, name="delete_review"),
    path("newsletter.html/", views.newsletter, name="newsletter"),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]