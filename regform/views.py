from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.sessions.models import Session 

# Create your views here.


def home(request):
    return render(request,'home.html')

def login(request):
    if request.session.get('is_logged',False):
        return redirect("home")
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            request.session['is_logged'] = True
            return redirect("home")
        else:
            messages.info(request,"Invalid username or password")
            return redirect("login")

    else:    
        return render(request, 'login.html')

def register(request):
    if request.session.get('is_logged',False):
        return redirect("home")
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        pwd1=request.POST['password1']
        pwd2=request.POST['password2']

        if pwd1==pwd2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'user already exists.')
                return redirect('register')

            elif User.objects.filter(email=email).exists():
                messages.info(request,'email already exists.')
                return redirect('register')
            else:
                user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username, password=pwd1, email=email)
                user.save()
        else:
            messages.info(request,'password not matching')
            return redirect('register')
        return redirect('login')

    else:
        return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')