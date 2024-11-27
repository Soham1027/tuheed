from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

def register(request):
    if request.method == 'POST':
        form = UserDataRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserDataRegisterForm()
    return render(request, 'register.html', {'form': form})

# Login View
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Redirect based on user type (Admin, Staff, or User)
                if user.is_superuser:  # Admin
                    return redirect('dashboard')
                elif user.join_type == '2':  # Staff
                    return redirect('#')
                elif user.join_type == '3':  # User
                    return redirect('add_staff')
            else:
                messages.error(request, 'Invalid username or password')
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


def dashboard2(request):
    if request.method == "GET":
        return render(request, "add_staff.html")