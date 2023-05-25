from django.shortcuts import render, HttpResponse
from . forms import UserForm
from . models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils.encoding import smart_str
from django.utils.encoding import force_bytes
# urlsafe_base64_encode() and urlsafe_base64_decode() functions in Django are used to encode and decode data in a way that is safe
# to use in URLs. The urlsafe_base64_encode() function takes a string as input and returns a base64-encoded string that does not
# contain any characters that are not allowed in URLs. The urlsafe_base64_decode() function takes a base64-encoded string as input
# and returns the original string, decoded from base64.
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# as i am not using django's default user so, i dont have last_login field so, can't generate tokens from PasswordResetTokenGenerator.
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# for making tokens
# for creating tokens...
from .uuid_gen import uuid_genrator
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.


def home(request):
    return render(request, "base.html", {"hii": "hello"})


def login(request):
    return render(request, 'login.html')


def activate(request, user_id, token):
    # uid = request.GET.get('user_id')
    uid = smart_str(urlsafe_base64_decode(user_id))
    user = User.objects.get(id=uid)
    if user:
        user.email_verification = 1
        user.save()
    return render(request, "login.html")


def login_logic(request):
    if request.method == "POST":
        email = request.POST['email']
        raw_password = request.POST['password']
        try:
            user_obj = User.objects.get(email=email)
            hashed_pasword = user_obj.password
            if user_obj:
                res = check_password(raw_password, hashed_pasword)

                if res and user_obj.email_verification == 1:
                    session_id = uuid_genrator()
                    user_obj.session_id = session_id
                    user_obj.save()
                    response = render(request, "dashboard.html", {
                                      "message": "login sucessful"})
                    response.set_cookie('session_id', session_id)
                    return response
        except:
            return render(request, "login.html", {"message": "incorrect email or password or verify ypur email first"})


def getcookies(request):
    value = request.COOKIES.get('session_id')
    return value


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

            '''urlsafe_base64_encode() and urlsafe_base64_decode( a bytes-like object is required, not 'str'or int) functions in Django are used to encode and decode 
            data in a way that is safe to use in URLs. The urlsafe_base64_encode() function takes a string as
            input and returns a base64-encoded string that does not contain any characters that are not allowed
            in URLs. The urlsafe_base64_decode() function takes a base64-encoded string as input and returns the
            original string, decoded from base64.'''
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            # token generator
            token = uuid_genrator()
            link = f"http://127.0.0.1:8000/activate/{user_id}/{token}/"
            subject = "Registration"
            email_content = f"Hi {user.username},\n\nThank you for signing up for our service. To verify your email address, please click on the following link:\n\n{link}\n\nIf you do not click on the link within 24 hours, your account will be deleted.\n\nThanks,\n[Django Bloggers]"
            email_from = settings.EMAIL_HOST_USER
            recepient_list = [email,]
            send_mail(subject, email_content, email_from, recepient_list)
            user = User(email_verification=1)
    return render(request, "login.html", {"message": "User register sucessfully..."})


def forget_passcode(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = User.objects.get(email=email)
        if user.exists():
            pass

    return render(request, "forgetpasscode.html")


def dashboard(request):
    val = getcookies(request)
    user = User.objects.get(session_id=val)
    if user:
        return render(request, "dashboard.html")
