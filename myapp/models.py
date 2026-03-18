from django.db import models
from django.contrib.auth.models import User

# Category model to group menu items
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# MenuItem model to represent each item on the menu
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=50) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

# Career model to represent job openings
class Career(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    job_emoji = models.CharField(max_length=10)
    def __str__(self):
        return self.title

# Review model to represent customer reviews 
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    rating = models.IntegerField() # 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.customer_name} - {self.rating} stars"

# ContactMessage model to represent messages sent through the contact form
class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} - {self.subject}"

# NewsletterSubscription model to represent newsletter subscribers
class NewsletterSubscription(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# Order and OrderItem models to represent customer orders and their items
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    items_summary = models.TextField(null=True, blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

# OrderItem model to represent each item in an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

# UserProfile model to represent additional user information
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    
    address = models.CharField(max_length=255, blank=True, null=True)
    telephone_number = models.CharField(max_length=20, blank=True, null=True)
    
    favorite_dessert = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# News model to represent news items for the about page
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# CartItem model to represent items in the user's cart 
class CartItem(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    

    
    