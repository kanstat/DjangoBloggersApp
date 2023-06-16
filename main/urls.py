from django.contrib import admin
from django.urls import path
from . import views
# for testing gunicor in production (DEBUG = True)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


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
    path('reset/', views.reset,
         name="reset"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('tinymce/', views.tinymce, name="tinymce"),
    path("view_blog/<id>", views.view_blog, name="view_blog"),
    path("edit_blog/<id>", views.edit_blog, name="edit_blog"),
    path("update_blog/<id>", views.update_blog, name="update_blog"),
    path("publish_url/<id>", views.publish_url, name="publish_url"),
    path("published_blog/<id>/<token>",
         views.published_blog, name="published_blog"),
    path("url_to_db/", views.url_to_db, name="url_to_db"),
]
urlpatterns += staticfiles_urlpatterns()
