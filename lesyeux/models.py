from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Neighborhood(models.Model):
    name = models.CharField(max_length=30, default='Unknown')
    location = models.CharField(max_length=100, default='Somewhere in Nairobi')
    population = models.CharField(max_length=128, default='Unknown')
    # admin  = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # businesses = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    # posts = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    police = models.CharField(max_length=12, default='911')
    ambulance = models.CharField(max_length=12, default='911')

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to='uploaded_images', blank=True)
    idnumber = models.CharField(max_length=10,)
    Neighborhood = models.ForeignKey(Neighborhood, blank = True)

class Business(models.Model):
    name = models.CharField(max_length=30, default='Unknown')
    image = models.ImageField(upload_to='business_images', blank=True)
    location = models.CharField(max_length=30, default='Unknown')
    additional_details = models.CharField(max_length=30)

class Post(models.Model):
    image_post = models.ImageField(upload_to='uploaded_images', blank=True)
    image_details = models.CharField(max_length=1000)
    text_post = models.CharField(max_length=1000)