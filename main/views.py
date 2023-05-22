from django.shortcuts import render,HttpResponse
from . forms import UserForm
from . models import User

# Create your views here.
def home(request):
    return render(request,"base.html",{"hii":"hello"})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        query = User.objects.filter(username=username,password=password)
        if query.exists():
            return render(request,"login.html",{"message":"login sucessful"})

    return render(request,"login.html",{"message":"Enter valid username and password"})
        
        


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        # form = UserForm(request.POST)
        # if form.is_valid():
            # extracting user data from form 
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password']
            # email = form.cleaned_data['email']
            # # creating user
        user = User(username=username,password=password,email=email)
            # save user into the database
        user.save()
    return render(request,"signup.html")