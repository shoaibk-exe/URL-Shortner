from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import URL
from .utils import generate_short_code


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'shortner/login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Account created!')
            return redirect('login')

    return render(request, 'shortner/signup.html')


@login_required
def dashboard(request):
    short_url = None

    if request.method == 'POST':
        original_url = request.POST.get('original_url')

        # Check if URL already exists for this user
        existing_url = URL.objects.filter(user=request.user, original_url=original_url).first()

        if existing_url:
            short_url = request.build_absolute_uri(existing_url.get_short_url())
        else:
            short_code = generate_short_code()
            new_url = URL.objects.create(
                user=request.user,
                original_url=original_url,
                short_code=short_code
            )
            short_url = request.build_absolute_uri(new_url.get_short_url())

    # Get all user's URLs for display
    urls = URL.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'shortner/dashboard.html', {
        'short_url': short_url,
        'urls': urls
    })


def redirect_to_original(request, code):
    url = get_object_or_404(URL, short_code=code)
    url.click_count += 1
    url.save()
    return redirect(url.original_url)
