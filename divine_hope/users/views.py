from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(response, "users/register.html", {"form": form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'users/login.html'


def profile(request):
    # Get the user's profile data if they are logged in
    if request.user.is_authenticated:
        user_profile = User.objects.get(username=request.user.username)
        return render(request, 'users/profile.html', {'user_profile': user_profile})
    else:
        # Handle the case when the user is not logged in
        return render(request, 'users/profile.html', {'user_profile': None})
