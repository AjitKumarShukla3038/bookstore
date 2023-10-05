from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout  # Changed the function name
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login as auth_login 
from django.views import generic
from django.urls import reverse_lazy
# from store.models import Customer

class UserRegistraion(generic.CreateView):
    form_class = NewUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            remember_me = form.cleaned_data.get('remember_me')
            if user is not None:
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks (in seconds)
                else:
                    request.session.set_expiry(0)
                auth_login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})

def logout(request):  # Renamed the view function
    auth_logout(request)  # Changed the function name
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


def changepassword(request):
    if request.method == "GET":
        # Create an instance of PasswordChangeForm for the user
        password_change_form = PasswordChangeForm(user=request.user)
        context = {'form': password_change_form}
        return render(request, 'changepass.html', context)

    elif request.method == "POST":
        # Create an instance of PasswordChangeForm with user data
        password_change_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            # Update the user's session after a password change
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect('/')  # Adjust the redirection URL as needed
        else:
            messages.error(request, "Invalid password change data. Please correct the errors.")
        
        context = {'form': password_change_form}
        return render(request, 'changepass.html', context)
