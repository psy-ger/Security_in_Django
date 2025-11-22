from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from .forms import RegistrationForm, LoginForm


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user_obj']
            # simple session usage
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            messages.success(request, f'Welcome {user.username}')
            return redirect('profile')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    # clear our custom session data
    request.session.flush()
    messages.info(request, 'Logged out')
    return redirect('login')


def profile(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    if not user_id:
        messages.warning(request, 'You must be logged in to access this page')
        return redirect('login')
    # Display user data (autoescaped in template)
    return render(request, 'accounts/profile.html', {'username': username})


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)
