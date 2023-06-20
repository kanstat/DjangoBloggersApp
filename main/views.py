from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse
from . forms import UserForm
from . models import Tinymce, User
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
from django.urls import reverse
from django.http import JsonResponse
import json

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
                    response = redirect("dashboard/")
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
            link = f"https://kantest.onrender.com/activate/{user_id}/{token}/"
            subject = "Registration"
            email_content = f"Hi {user.username},\n\nThank you for signing up for our service. To verify your email address, please click on the following link:\n\n{link}\n\nIf you do not click on the link within 24 hours, your account will be deleted.\n\nThanks,\nDjango Bloggers"
            email_from = settings.EMAIL_HOST_USER
            recepient_list = [email,]
            send_mail(subject, email_content, email_from, recepient_list)
            user = User(email_verification=1)
    return render(request, "login.html", {"message": "User register sucessfully..."})


def forget_passcode(request):
    return render(request, "forgetpasscode.html")


def forgot_password_logic(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = User.objects.get(email=email)
    if user:
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = uuid_genrator()
        reset_link = f"https://kantest.onrender.com/reset?uid={uid}&token={token}/"
        subject = "Password reset link"
        email_content = f"Hi {user.username},\n\nThank you for signing up for our service. To verify your email address, please click on the following link:\n\n{reset_link}\n\nIf you do not click on the link within 24 hours, your account will be deleted.\n\nThanks,\nDjango Bloggers"
        email_from = settings.EMAIL_HOST_USER
        recepient_list = [email,]
        send_mail(subject, email_content, email_from, recepient_list)
    return render(request, "forgetpasscode.html", {"message": "Password reset link has been send successfully"})


def reset(request):
    if request.method == "GET":
        return render(request, "reset_logic.html")
    if request.method == "POST":
        password = request.POST["psw1"]
        password2 = request.POST["psw2"]
        uid = request.POST['uid']
        token = request.POST['token']

        if password == password2 and uid is not None:
            decode_uid = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=decode_uid)
            if user:
                user.password = make_password(password)
                user.save()
            else:
                return render(request, "reset_logic.html", {"message": "User does not exists"})
        else:
            return render(request, "reset_logic.html", {"message": "Password do not match"})
    return render(request, "login.html", {"message": "Password changed sucessfully.."})


def dashboard(request):
    val = getcookies(request)
    user = User.objects.get(session_id=val)
    blog = Tinymce.objects.filter(user_fk=user)

    context = {"blog": blog, "user_name": user.username}
    if user:
        return render(request, "dashboard.html", context)


def tinymce(request):
    if request.method == "GET":
        return render(request, "tinymce.html")

    if request.method == "POST":
        val = getcookies(request)
        user = User.objects.get(session_id=val)
        content = request.POST["textarea"]
        blog_title = request.POST["blogTitle"]
        tinymce_obj = Tinymce.objects.create(
            content=content, user_fk=user, title=blog_title)
        tinymce_obj.save()
    return render(request, "dashboard.html")


def view_blog(request, id):
    val = getcookies(request)
    blog = Tinymce.objects.get(id=id)
    context = {"blog": blog.content, "date": blog.created_at, "id": blog.id}
    return render(request, "blog_view.html", context)


def edit_blog(request, id):
    val = getcookies(request)
    blog = Tinymce.objects.get(id=id)
    context = {"blog_content": blog.content,
               "date": blog.created_at, "blogTitle": blog.title, "id": blog.id}
    return render(request, "edit_blog.html", context)


def update_blog(request, id):
    val = getcookies(request)
    user = User.objects.get(session_id=val)
    if user:
        blog_to_edit = Tinymce.objects.get(id=id)

        blog_content = request.POST["textarea"]
        blog_title = request.POST["blogTitle"]

        blog_to_edit.title = blog_title
        blog_to_edit.content = blog_content
        blog_to_edit.save()
    return redirect(reverse('view_blog', kwargs={'id': id}))


def publish_url(request, id):
    val = getcookies(request)
    user = User.objects.get(session_id=val)
    rndm = uuid_genrator()
    if user:
        blog = Tinymce.objects.get(id=id)
        if blog.published_url == '':
            published_url = f"127.0.0.1:8000/published_blog/{id}/{rndm}"
            blog.published_url = published_url
            blog.pub_url_active = True
            blog.save()

    # return (request,)


# def published_blog(request, id, token):
#     blog = Tinymce.objects.get(id=id)
#     context = {"blog": blog.content, "date": blog.created_at, "id": blog.id}
#     return render(request, "published_blog.html", context)


def url_to_db(request, id):
    blog_id = int(id)
    blog = Tinymce.objects.get(id=blog_id)
    if blog.pub_url_active == False:
        rndm = uuid_genrator()
        # rndm = rndm[1:7]
        published_url = f"127.0.0.1:8000/published_blog/{id}/{rndm}"
        blog.published_url = published_url
        blog.pub_url_active = True
        blog.save()
        data = {"published_url": published_url}
    elif blog.pub_url_active == True:
        published_url = blog.published_url
        data = {"published_url": published_url}
    return JsonResponse(data)


def change_perm(request, id):
    blog_id = int(id)
    blog = Tinymce.objects.get(id=blog_id)
    user = blog.user_fk
    permissions = request.body
    permissions = json.loads(permissions)
    read_perm = permissions['new_read']
    write_perm = permissions['new_write']
    if user:
        user.read_permission = read_perm
        user.write_permission = write_perm
        user.save()
        return redirect(reverse('view_blog', kwargs={'id': id}))
    else:
        return render(request, "not_found404.html")


def published_blog(request, id, token):
    blog = Tinymce.objects.get(id=id)
    user = blog.user_fk
    read_perm = user.read_permission
    write_perm = user.write_permission
    context = {"blog": blog.content, "date": blog.created_at,
               "id": blog.id, "read_perm": read_perm, "write_perm": write_perm}
    try:
        if read_perm == "everyone":
            return render(request, "published_blog.html", context)
        elif read_perm == 'signed-in-users':
            val = getcookies(request)
            user = User.objects.get(session_id=val)
            if user:
                return render(request, "published_blog.html", context)
            else:
                return redirect('login/')
        elif read_perm == 'onlyme':
            val = getcookies(request)
            user_ = User.objects.get(session_id=val)
            user = blog.user_fk
            if user == user_:
                return render(request, "published_blog.html", context)
    except:
        return render(request, "not_found404.html")
