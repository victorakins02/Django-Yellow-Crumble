from django.contrib import admin

from .models import MenuItem, Career, Category, UserProfile

admin.site.register(MenuItem)
admin.site.register(Career)
admin.site.register(Category)
admin.site.register(UserProfile)
