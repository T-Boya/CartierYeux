from django.contrib import admin
from django.contrib.auth.models import User
from lesyeux.models import Neighborhood, Business, Post, UserProfile

# Register your models here.
admin.site.register(Neighborhood)
admin.site.register(Business)
admin.site.register(Post)
admin.site.register(UserProfile)
