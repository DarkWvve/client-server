from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .form import RegisterCustomerForm


def register_customer(request):
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_customer = True
            var.save()
            messages.success(request, 'Your account has been Successfully registered. Please login to continue')
            return redirect('login')
        else:
            messages.warning(request, "somthing went wrong, please enter correct information")
            return redirect('register-customer')
    else:
        form = RegisterCustomerForm()
        context = {
            'form': form
            }
        return render(request, 'users/register_customer.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, 'Login Successfully. Please enjoy your session')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong. Please check your credentials')
            return redirect('login')
    else:
        return render(request, 'users/login.html')




def logout_user(request):
    logout(request)
    messages.success(request, 'Your session has been ended. Please login to continue')
    return redirect('login')
