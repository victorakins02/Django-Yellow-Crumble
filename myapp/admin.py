from django.contrib import admin

from .models import MenuItem, Career, Category, UserProfile, News

admin.site.register(MenuItem)
admin.site.register(Career)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(News)