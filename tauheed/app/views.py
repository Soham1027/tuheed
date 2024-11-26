from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful!")
            return redirect('login')  # Redirect to the login page after successful registration
        else:
            messages.error(request, "There were errors in your form. Please check.")
    else:
        form = UserRegistrationForm()
    
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form.is_valid())
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username)

            # Try to find the user in the UserData model
            try:
                user = UserData.objects.get(username=username)  # Retrieve user by username
            except UserData.DoesNotExist:
                user = None

            # Check if the user exists and if the password matches
            print(user.password)
            print(check_password(password, user.password))
            if user and password==user.password:  # Password check
            
                if user:  # Check if the user is active
                    login(request, user)  # Log in the user
                    return redirect('dashboard')  # Redirect to the dashboard or home page
                
                else:
                    messages.error(request, "Account is disabled.")
            else:
                messages.error(request, "Invalid username or password.")

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if "user_id" in request.session:
        del request.session["user_id"]
        del request.session["username"]
    messages.success(request, "You have successfully logged out.")
    return redirect("login")



@login_required
def add_staff(request):
    # Restrict access to admin users only
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to add staff.")
        return redirect('dashboard')  # Replace 'dashboard' with the appropriate URL name
    
    if request.method == "POST":
        form = AddStaffForm(request.POST)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.user_type = 'BACK_STAFF_USER'  # Set user type to Back Staff
            staff.save()

            messages.success(request, "Staff member added successfully!")
            return redirect('add_staff') 
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AddStaffForm()

    return render(request, "add_staff.html", {"form": form})



def dashboard(request):
    if request.method == "GET":
        return render(request, "dashboard.html")
    
    else:
        print("wrong")
    return render (request, "login.html" )