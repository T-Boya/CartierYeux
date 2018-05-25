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