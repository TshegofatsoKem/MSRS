from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def staff_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('worker_dashboard')
        else:
            error = 'Invalid username or password. Please try again.'
    return render(request, 'accounts/login.html', {'error': error})


def staff_logout(request):
    logout(request)
    return redirect('home')