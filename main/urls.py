from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('loginpg/', views.login, name='login'),
    path('login_logic', views.login_logic, name="login_logic"),
    path('activate/<user_id>/<token>/', views.activate, name="activate"),
    path('signuppg/', views.signup, name="signup"),
    path('signup_logic/', views.signup_logic, name='signup_logic'),
    path('forgot_password/', views.forget_passcode, name='forget_passcode'),
    path('forgot_password_logic/', views.forgot_password_logic,
         name="forgot_password_logic"),
    path('reset/<user_id>/<token>', views.forgot_password_validation,
         name="forgot_pass_validation"),
    path('dashboard/', views.dashboard, name="dashboard"),
]
