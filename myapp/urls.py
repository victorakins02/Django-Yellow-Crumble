from django.urls import path
from . import views 

# URL patterns for the myapp application
urlpatterns = [
    path("", views.home, name="home"), # Home page with reviews and menu items
    path("index.html/", views.index, name="index"), # Main page with menu and cart
    path("login.html/", views.login, name="login"), # Login page
    path("about.html/", views.about, name="about"), # About page with news and company info
    path("contact.html/", views.contact, name="contact"), # Contact page with form
    path("faq.html/", views.faq, name="faq"), # FAQ page with common questions and answers
    path("careers.html/", views.careers, name="careers"), # Careers page with job listings
    path("gallery.html/", views.gallery, name="gallery"), # Gallery page with images of food and restaurant
    path("reviews.html/", views.review, name="review"),  # Reviews page with customer reviews and form to submit new review
    path("edit-review/<int:review_id>/", views.edit_review, name="edit_review"), # Edit review page to allow users to edit their reviews
    path("delete-review/<int:review_id>/", views.delete_review, name="delete_review"), # Delete review page to allow users to delete their reviews
    path("newsletter.html/", views.newsletter, name="newsletter"), # Newsletter subscription page with form to subscribe to newsletter
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'), # Add to cart page to handle adding items to the cart
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'), # Remove from cart page to handle removing items from the cart
    path('register/', views.register, name='register'), # Registration page to handle user registration
    path('login/', views.login_view, name='login'), # Login page to handle user login
    path('logout/', views.logout_view, name='logout'), # Logout page to handle user logout
    path('profile/', views.profile_view, name='profile'), # Profile page to display user information and order history
    path('submit-order/', views.submit_order, name='submit_order'), # Submit order page to handle order submission and processing
]