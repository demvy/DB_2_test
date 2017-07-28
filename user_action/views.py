from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import UserForm, VerifyForm, LoginForm
from django.contrib import messages
from .models import User
from .models import Profile
from db_2_test.settings import EMAIL_HOST_USER


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            email = user_form.cleaned_data['email']
            passwd = user_form.cleaned_data['password']
            log = User.objects.create(username='users'+email, email=email, password=passwd)
            log.set_password(passwd)
            log.save()
            log.profile = Profile.objects.create(user=log)
            log.save()
            subject = 'Registration at Post testing app'
            message = 'Welcome to our app-social network!\nEnjoy your time.\nYour verification code: '\
                       + log.profile.verification_code
            from_email = EMAIL_HOST_USER
            to_list = [log.email]
            send_mail(subject, message, from_email, to_list, fail_silently=False)
            messages.success(request, 'Thank you for registration, check your email and verify your account')
            return redirect('user:verify')
        else:
            return render(request, 'register.html', {'user_form': user_form})
    else:
        user_form = UserForm()
    return render(request, 'register.html', {'user_form': user_form})


@csrf_protect
def user_login(request):
    logout(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            verified = User.objects.get(email=form.cleaned_data['email']).profile.verified
            if verified:
                email = form.cleaned_data['email']
                print('user'+email, form.cleaned_data['password'])
                if User.objects.get(username='users'+email):
                    print("success")
                user = authenticate(username='users'+email, password=form.cleaned_data['password'])
                if user:
                    if user.is_active:
                        login(request, user)
                        return redirect('/net/')
                else:
                    form.add_error('email', 'No such email')
            else:
                messages.error(request, 'Verify your email!')
                return redirect('user:verify')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


@csrf_protect
def verify_email(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['email'])
            code = form.cleaned_data['code']
            if code == user.profile.verification_code:
                profile = Profile.objects.get(user=user.id)
                profile.verified = True
                profile.save()
                return redirect('/')
            else:
                form.add_error('code', "Not right verification code!")
        else:
            return render(request, 'verify.html', {'form': form})
    else:
        form = VerifyForm()
    return render(request, 'verify.html', {'form': form})