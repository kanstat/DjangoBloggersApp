from django.shortcuts import render, HttpResponse
from . forms import UserForm
from . models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here.


def home(request):
    return render(request, "base.html", {"hii": "hello"})


def login(request):
    return render(request, 'login.html')


def login_logic(request):
    if request.method == "POST":
        email = request.POST['email']
        raw_password = request.POST['password']
        try:
            user_obj = User.objects.get(email=email)
            hashed_pasword = user_obj.password
            if user_obj:
                res = check_password(raw_password, hashed_pasword)
                if res:
                    return render(request, "dashboard.html", {"message": "login sucessful"})
        except:
            return render(request, "login.html", {"message": "incorrect email or password"})


def signup(request):
    return render(request, "signup.html")


def signup_logic(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = make_password(request.POST["password"])
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


def dashboard(request):
    return render(request, "dashboard.html")
