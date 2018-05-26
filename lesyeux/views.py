from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from lesyeux.forms import SignupForm, UserProfileForm, NeighborhoodForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from lesyeux.tokens import account_activation_token
from django.contrib.auth.models import User
from lesyeux.models import Neighborhood, UserProfile, Business, Post
from django.core.mail import EmailMessage
from django.views.decorators.http import require_POST

def index(request):
    return HttpResponse('Home sweet home')

def signup(request):
    if request.method == 'POST':
        user_form = SignupForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            print('1')

            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                profile.save()
                registered = True
                email.send()
            else:
                email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

    else:
        user_form = SignupForm()
        profile_form = UserProfileForm(data = request.POST)
    return render(request, 'signup.html', {'user_form': user_form, 'profile_form': profile_form,})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect('nieghborhoods')

            else:
                return HttpResponse("Your account is disabled.")

        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        # return HttpResponse('gegeegegeg')
        return render(request, 'login.html')

@login_required
def create_neighborhood(request):
    form = NeighborhoodForm()
    if request.method == 'POST':
        form = NeighborhoodForm(request.POST, request.FILES)
        if form.is_valid():
            neighborhood = Neighborhood(image = request.FILES['image'])
            neighborhood = form.save(commit=True)
            return redirect('neighborhoods')
    else:
        print(form.errors)
    return render(request, 'new_neighborhood.html', context = {'form':form,})

@login_required
def neighborhoods(request):
    neighborhoods = Neighborhood.objects.all()
    # for neighborhood in neighborhoods:
    #     redirect = neighborhood.get_url
    return render(request, 'view_neighborhoods.html', context = {'neighborhoods' : neighborhoods,})

@login_required
def show_neighborhood(request, id=None):
    neighborhood = get_object_or_404(Neighborhood, id=id)
    return render(request,'show_neighborhood.html', context = {'neighborhood' : neighborhood,})
    # return render(request, 'Instagram/details.html', context = {'nieghborhood' : neighborhood,})