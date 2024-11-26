from django.urls import path
from .views import *

urlpatterns = [
    
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    
    
    
    ##############Back Panel Staff member################
    path("add_staff/", add_staff, name="add_staff"),
]
