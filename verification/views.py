from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.urls import reverse
import random

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            request.session['verification_code'] = random.randint(100000, 999999)
            email = EmailMessage(
                'Verify your email address',
                f'Your verification code is: {request.session["verification_code"]}',
                'noreply@example.com',
                [user.email],
            )
            email.send()
            return redirect('verify_email')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def verify_email(request):
    if request.method == 'POST':
        verification_code = request.session.get('verification_code')
        if verification_code == int(request.POST.get('verification_code')):
            user = User.objects.get(email=request.POST.get('email'))
            user.is_active = True
            user.save()
            del request.session['verification_code']
            return redirect('login')
    return render(request, 'verify_email.html')



def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('home')



def home(request):
    return render(request, 'home.html')



def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            request.session['verification_code'] = random.randint(100000, 999999)
            email = EmailMessage(
                'Reset your password',
                f'Your verification code is: {request.session["verification_code"]}',
                'noreply@example.com',
                [user.email],
                reply_to=[f'{request.scheme}://{request.get_host()}{reverse("password_reset_confirm")}?email={email}']
            )
            email.send()
            return redirect('verify_password_reset_email')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})

def verify_password_reset_email(request):
    if request.method == 'POST':
        verification_code = request.session.get('verification_code')
        if verification_code == int(request.POST.get('verification_code')):
            email = request.GET.get('email')
            return redirect(reverse('password_reset_confirm') + f'?email={email}')
    return render(request, 'verify_password_reset_email.html')
