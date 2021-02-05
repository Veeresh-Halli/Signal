from django.shortcuts import render,redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.cache import cache
from .models import LoggedUsers

# Create your views here.

def index(request):
    if request.session.has_key('username'):
        return redirect('dashboard')
    else:
        return redirect('loginpage')
    return render(request, 'index.html')

def register(request):
    if request.session.has_key('username'):
        return redirect('dashboard')
    else:
     form = CreateUserForm()
    
     if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was successfully created for "+ user)
            return redirect('loginpage')
        else:
            messages.error(request,"Passwords are not matching...")
            return redirect('register')
    context = {
        'form': form
    }
    return render(request, 'register.html', context)

def LoginPage(request):
    if request.session.has_key('username'):
         return redirect('dashboard')
    else:
      if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect('dashboard')
        else:
            messages.error(request,"username or password is incorrect....")
            return redirect('loginpage')
    return render(request, 'loginpage.html')

def LogoutPage(request):
    if request.session.has_key('username'):
        logout(request)
        request.session.flush()
        return redirect('loginpage')
    else:
        return redirect('register')

def dashboard(request):
    if request.session.has_key('username'):
       users = User.objects.all().count()
       username = request.session.get('username')
       active_users = LoggedUsers.objects.all().count()
       user = request.user
       ip = request.session.get('ip')
       browser = request.session.get('browser')
       count1 = cache.get('count1', version=user.pk)
       count = cache.get('count')
    else:
        return redirect('loginpage')
    context = {
        'username':username,
        'ip':ip,
        'count' : count,
        'count1' : count1,
        'users' : users,
        'active_users':active_users,
        'browser':browser,
    }
    return render(request, 'dashboard.html',context)

def UsersPage(request):
    if request.session.has_key('username'):
      users_count = User.objects.all().count()
      username = request.session.get('username')
      user = Session.objects.values('session_data')
      active_users = LoggedUsers.objects.all().order_by('user')
      
    else:
        return redirect('loginpage')
    context = {
        'username': username,
        'users_count': users_count,
        'user' : user,
        'active_users':active_users
    
    }
    return render(request, 'users.html',context)