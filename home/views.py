from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Tickers, User

# Create your views here.
def index(request):
    tickers = Tickers.objects.all()  
    return render(request, "home/index.html", {
        'tickers': tickers 
    })

def under(request):
    return render(request, 'home/under.html')

    


def signup(request):
    if request.method == "POST":

        username = request.POST["username"].strip()
        email = request.POST["email"].strip().lower()
        password = request.POST["password"].strip()
        confirmation = request.POST["confirmation"].strip()
        
        # Validate Username, password
        existingusers = User.objects.values_list('username', flat=True)
        existingmails = User.objects.values_list('email', flat=True)

        if username in existingusers:
            return render(request, "home/signup.html", {
                "message": "Username is already taken",
                'username': username,
                'email' : email
            })
        elif email in existingmails:
            return render(request, "home/signup.html", {
                "message": "Email already exists, Try loging in",
                'username': username,
                'email' : email
            })
        elif username == '' or len(username) < 5 or len(username) > 20:
            return render(request, "home/signup.html", {
                "message": "Username must be minimum of 5 characters and Maxium of 20 characters",
                'username': username,
                'email' : email
            })
        elif ' ' in username:
            return render(request, "home/signup.html", {
                "message": "Username must not contain spaces",
                'username': username,
                'email' : email
            })
        

        #Validate password

        if len(password) < 8:
            return render(request, "home/signup.html", {
                "message": "Password must be atleast 8 characters long",
                'username': username,
                'email' : email
            })
        elif ' ' in password:
            return render(request, "home/signup.html", {
                "message": "Password must not have spaces"
            })
        elif password != confirmation:
            return render(request, "home/signup.html", {
                "message": "Passwords did not match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "home/signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return render(request, 'home/index.html')
    else:
        return render(request, "home/signup.html")

def signin(request):
    if request.method == "POST":
        email = request.POST["email"].strip().lower()
        password = request.POST["password"].strip()

        user = authenticate(username = email, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return render(request, 'home/index.html')
        return render(request, 'home/signup.html', {"message": "login failed"})   
    elif request.method == 'GET':
        return render(request, "home/signin.html")

def signout(request):
    logout(request)
    return render(request, 'home/index.html')


def profile(request):
    return render(request, 'home/profile.html')
    
def details(request, id):
    item = Tickers.objects.get(id = id)
    return render(request, 'home/details.html', {
        'item': item
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"].strip().lower()
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "home/signup.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "home/signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "home/signup.html")