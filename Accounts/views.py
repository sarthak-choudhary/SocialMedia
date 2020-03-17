from django.shortcuts import render
from Accounts.forms import UserCreateForm
from django.contrib.auth.models import User

#for login functionality
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def index(request):
    return render(request,'index.html')

@login_required
def user_logout(request):
    logout(request)
    return render(request,'index.html')

def register(request):
    registered = False
    if request.method =="POST":
        user_form = UserCreateForm(data=request.POST)

        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password1']
            user = User(username=username,email=email)
            user.set_password(password)
            user.save()
            user.refresh_from_db()
            user.profile.first_name = user_form.cleaned_data['first_name']
            user.profile.last_name = user_form.cleaned_data['last_name']
            user.profile.birthdate = user_form.cleaned_data['birthdate']
            user.profile.save()
            #print(user.password)
            registered = True
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse('social:home'))
        else:
           print(user_form.errors)
    else:
        user_form = UserCreateForm()
    
    return render(request,'registration.html',
                            {'user_form':user_form,
                            'registered':registered})


def user_login(request):    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username,password=password)
        if user:
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse('index'))
        else:
            print("someone tried to login and failed!!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied! ")    
    else:
        return render(request,'login.html',{})
