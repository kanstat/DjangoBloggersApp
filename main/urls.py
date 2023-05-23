from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('loginpg/', views.login, name='login'),
    path('signuppg/', views.signup, name="signup"),
    path('signup_logic/', views.signup_logic, name='signup_logic'),
    path('forgot_password/', views.forget_passcode, name='forget_passcode'),
]
