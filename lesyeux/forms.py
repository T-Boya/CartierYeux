from django import forms
from django.contrib.auth.forms import UserCreationForm
from lesyeux.models import UserProfile, Neighborhood, Business, Post
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('idnumber', 'image')

class NeighborhoodForm(forms.ModelForm):
    image = forms.FileField(label='Select an image file', help_text='Please select a photo to upload')
    name = forms.CharField(help_text="Please enter the name of the neighborhood.")
    location = forms.CharField(help_text="Please enter the location.")
    population = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    police = forms.CharField(help_text="Please enter the police department phone number.")
    ambulance = forms.CharField(help_text="Please enter the ambulance phone number.")

    class Meta:
        model = Neighborhood
        fields = ('image', 'name', 'location', 'population', 'police', 'ambulance')