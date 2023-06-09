from django.contrib import admin
from django.urls import path
from . import views
# for testing gunicor in production (DEBUG = True)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from main.views import UserAuthView, ViewBlogContent

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
    path("url_to_db/<id>/", views.url_to_db, name="url_to_db"),
    path("change_perm/<id>/", views.change_perm, name="change_perm"),
    path("link/", UserAuthView.as_view(), name="link_tg"),
    path("view_blog_api/", ViewBlogContent.as_view(), name="view_blog_api")
]
urlpatterns += staticfiles_urlpatterns()
