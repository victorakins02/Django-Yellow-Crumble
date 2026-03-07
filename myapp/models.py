from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Career(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    job_emoji = models.CharField(max_length=10)
    def __str__(self):
        return self.title
    
class Review(models.Model):
    name = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.IntegerField()
    def __str__(self):
        return self.name
    
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
#     address = models.CharField(max_length=255, blank=True, null=True)
#     telephone_number = models.CharField(max_length=20, blank=True, null=True)
    
#     favorite_dessert = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return f"{self.user.username}'s Profile"