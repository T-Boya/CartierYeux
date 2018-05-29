from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from lesyeux.forms import SignupForm, UserProfileForm, NeighborhoodForm, PostForm, BusinessForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from lesyeux.tokens import account_activation_token
from django.contrib.auth.models import User
from lesyeux.models import Neighborhood, UserProfile, Business, Post
from django.core.mail import EmailMessage
from django.views.decorators.http import require_POST
from itertools import chain

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
            subject = 'Activate Your Account'
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
            profile.save()
            registered = True
            user.email_user(subject, message)
            # next = request.POST.get('next', '/')
            return HttpResponse('Please confirm your email to login.')              
            # return HttpResponse('Please confirm your email address to complete the registration')

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
        username=user.username
        password=user.password
        user = authenticate(username=username, password=password)
        # return redirect('index')
        return render(request, 'activated.html')
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
                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)

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
    form = BusinessForm()
    all_businesses = Business.objects.all()
    businesses = all_businesses.filter(neighborhood_id=id)
    print(businesses)
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = Business(image = request.FILES.get('image'))
            business = form.save(commit=False)
            business.neighborhood = neighborhood
            business = business.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        form = BusinessForm()
    return render(request,'show_neighborhood.html', context = {'form' : form, 'neighborhood' : neighborhood, 'businesses':businesses})

@login_required
def view_business(request, id=None):
    business = get_object_or_404(Business, id=id)
    return render(request,'view_business.html', context = {'business':business})

def index(request):
    neighborhoods = Neighborhood.objects.all().order_by('-id')[:4]
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
            email.send()
            return HttpResponse('Please confirm your email to login.')


    else:
        user_form = SignupForm()
        profile_form = UserProfileForm(data = request.POST)
        return render(request,'home.html', context = {'neighborhoods' : neighborhoods, 'user_form': user_form, 'profile_form': profile_form,})
    return render(request,'home.html', context = {'neighborhoods' : neighborhoods, 'user_form': user_form, 'profile_form': profile_form,})


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def posts(request, id=None):
    neighborhood = get_object_or_404(Neighborhood, id=id)
    form = PostForm()
    all_posts = Post.objects.all().order_by('-id')
    posts = all_posts.filter(neighborhood_id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post(image = request.FILES.get('image'))
            post = form.save(commit=False)
            post.author = request.user
            post.neighborhood = neighborhood
            post = post.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        form = PostForm()
    return render(request, 'posts.html', context = {'form':form, 'posts':posts, 'neighborhood':neighborhood,})

def search(request):
    if 'contains' in request.GET and request.GET["contains"]:
            query = request.GET.get("contains")
            businesses = Business.search(query)
            neighborhoods = Neighborhood.search(query)
            results = list(chain(neighborhoods, businesses))
            output = f"{query}"

            return render(request,'search.html',{"output":output, "results":results})

    else:
        message = "You haven't searched for anything"
        return render(request, 'search.html',{"message":message})
    return render(request, 'search.html',)

@login_required
def edit_neighborhood(request, id = None):
    neighborhood = get_object_or_404(Neighborhood, id=id)
    n_id = neighborhood.id
    if request.method == 'POST':
        neighborhood.name = request.POST.get('name')
        neighborhood.location = request.POST.get('location')
        neighborhood.population = request.POST.get('population')
        neighborhood.police = request.POST.get('police')
        neighborhood.ambulance = request.POST.get('ambulance')
        if request.FILES == True:
            neighborhood.image = request.FILES.get('image')
            update_neighborhood = neighborhood.save()
            return redirect('show_neighborhood', id=n_id)
        else:
            update_neighborhood = neighborhood.save() 
            return redirect('show_neighborhood', id=n_id)
    else:
        return render(request, 'edit_neighborhood.html', {'neighborhood':neighborhood, 'n_id' : n_id,})
    return render(request, 'edit_neighborhood.html', {'neighborhood':neighborhood, 'n_id' : n_id,})

@login_required
def delete_neighborhood(request, id = None):
    neighborhood = get_object_or_404(Neighborhood, id=id)
    neighborhood.delete_neighborhood()
    return redirect('neighborhoods')

@login_required
def view_user(request, id = None):
    user = get_object_or_404(User, id=id)
    return render(request, 'view_user.html', {'user':user})
