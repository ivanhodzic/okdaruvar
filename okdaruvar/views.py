from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from trainings.models import Trainer, Club
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from okdaruvar.email import send_email, is_valid_email
import secrets
import string
from django.db.models import Q

def index(request):   
    return render(request,'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if is_valid_email(username):
            try:
                u=User.objects.get(email=username)
                username=u.username
            except User.DoesNotExist:
                pass
        print(username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('hometrainer')
        else:
            messages.error(request, 'Invalid username or password', extra_tags='alert-danger')
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('')

def forgot_password_view(request):
    club = Club.objects.first()
    context = {
        'club_name':club.club_name
    }
    return render(request, 'forgot-password.html',context)

def recover_password_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        print(username)
        try:
            user = User.objects.filter(Q(username=username) | Q(email=username)).first()
            if user is None:

                raise User.DoesNotExist
            #GENERATE RANDOM PASSWORD
            characters = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(secrets.choice(characters) for _ in range(10))
    
            user.set_password(password)
            user.save()
            #SEND EMAIL
            send_email("OK Daruvar - password change",f"Your new password is:{password}", user.email)
            print(password)
            messages.success(request, 'Mail uspješno poslan!', extra_tags='alert-success')
            return redirect('index')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username', extra_tags='alert-danger')
    return redirect('forgot-password')
       

def changed_password_view(request):
    username = request.session.get('user_username')
    user = User.objects.get(username=username)
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:         
            user.set_password(password1)
            user.save()
            return redirect('index')
        else:
            messages.error(request, 'Passwords doesnt match!')
    
    context = {
        'user':user.username
    }
    return render(request, 'recover-password.html',context)
            
            
       
    