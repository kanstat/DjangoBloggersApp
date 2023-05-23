from django.shortcuts import render, HttpResponse
from . forms import UserForm
from . models import User
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here.


def home(request):
    return render(request, "base.html", {"hii": "hello"})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        query = User.objects.filter(username=username, password=password)
        if query.exists():
            return render(request, "login.html", {"message": "login sucessful"})

    return render(request, "login.html", {"message": "Enter valid username and password"})


def signup(request):
    return render(request, "signup.html")


def signup_logic(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        if User.objects.filter(email=email).exists():
            return render(request, "signup.html", {"message": "This email already exits try with new email.."})
        # save user into the database
        else:
            user = User(username=username, password=password, email=email)
            user.save()
    return render(request, "login.html", {"message": "User register sucessfully..."})


def forget_passcode(request):
    if request.method == "POST":
        email = request.POST["email"]
        if User.objects.filter(email=email).exists():
            # user_obj =
            pass
    return render(request, "forgetpasscode.html")
