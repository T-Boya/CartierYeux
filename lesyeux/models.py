from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.template.defaultfilters import slugify

# Create your models here.
class Neighborhood(models.Model):
    image = models.ImageField(upload_to='neighborhood_photos', null=True)
    name = models.CharField(max_length=30, default='Unknown', blank=True)
    location = models.CharField(max_length=100, default='Somewhere in Nairobi', blank=True)
    population = models.CharField(max_length=128, default='Unknown', blank=True)
    # admin  = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # businesses = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    # posts = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    police = models.CharField(max_length=12, default='911', blank=True)
    ambulance = models.CharField(max_length=12, default='911', blank=True)
    # slug = models.SlugField(unique=True, blank = True)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Neighborhood, self).save(*args, **kwargs)

    # def get_url(self):
    #     return redirect("show_neighborhood", kwargs={"slug" : self.slug})

    def get_url(self):
        return redirect("show_neighborhood", kwargs={"id" : self.id})

    def delete_neighborhood(self):
        self.delete()

    @classmethod
    def search(cls, query):
        neighborhood = cls.objects.filter(name__icontains=query)
        return neighborhood

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to='user_dps', blank=True)
    idnumber = models.CharField(max_length=10,)
    neighborhood = models.ForeignKey(Neighborhood, blank = True)

class Business(models.Model):
    name = models.CharField(max_length=30, default='Unknown')
    image = models.ImageField(upload_to='business_images', blank=True)
    location = models.CharField(max_length=30, default='Unknown')
    additional_details = models.CharField(max_length=30, blank=True)
    neighborhood = models.ForeignKey(Neighborhood)

    @classmethod
    def search(cls, query):
        business = cls.objects.filter(name__icontains=query)
        return business

class Post(models.Model):
    image = models.ImageField(upload_to='uploaded_images', blank=True, null=True)
    text_post = models.CharField(max_length=1000)
    author = models.ForeignKey(User)
    neighborhood = models.ForeignKey(Neighborhood)