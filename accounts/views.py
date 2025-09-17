from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    # Dummy form handling (does not authenticate)
    if request.method == 'POST':
        # Always fail standard login (per requirements)
        messages.error(request, 'Invalid username or password. Please use Sign in with Microsoft.')
        return redirect('accounts:login')

    return render(request, 'accounts/login.html')


def sso_start(request: HttpRequest) -> HttpResponse:
    # Stub: In real Azure AD SSO, redirect to Microsoft authorization endpoint with state/nonce
    # Here, we simulate immediate return to callback with success
    return redirect('accounts:sso_callback')


def sso_callback(request: HttpRequest) -> HttpResponse:
    # Stub: In real flow, validate state, exchange code for tokens, fetch user info
    try:
        # Simulate retrieving or creating a user from SSO claims
        email = 'john.doe@example.com'
        username = 'john.doe'

        user, _ = User.objects.get_or_create(username=username, defaults={'email': email})
        user.is_active = True
        user.save()

        login(request, user)
        messages.success(request, 'Signed in with Microsoft successfully.')
        return redirect('dashboard:index')
    except Exception:
        messages.error(request, 'SSO sign-in failed. Please try again later.')
        return redirect('accounts:login')


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')
