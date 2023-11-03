from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Tickers, User
from forum.models import Topic, Comment
import csv
import os
import yfinance as yf

def go_back(request):
    # Get the HTTP_REFERER from the request's META information
    previous_page = request.META.get('HTTP_REFERER')
    
    if previous_page:
        # If the HTTP_REFERER is available, redirect to it
        return redirect(previous_page)
    else:
        # If there's no previous page, redirect to a default URL or handle it accordingly
        return redirect('index')


def Get_All_Tickers():
    tickers = Tickers.objects.all()
    return tickers

def index(request):
    tickers = Get_All_Tickers()
    return render(request, "home/index.html", {
        'tickers': tickers
    })


def signup(request):
    if request.method == "POST":

        username = request.POST["username"].strip()
        email = request.POST["email"].strip()
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
        email = request.POST["email"].strip()
        password = request.POST["password"].strip()

        user = authenticate(username = email, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect('home')
        return render(request, 'home/signup.html', {"message": 'User not found, Try signing up'})   
    elif request.method == 'GET':
        return render(request, "home/signin.html")

def signout(request):
    logout(request)
    return redirect('home')

def profile(request):
    return render(request, 'home/profile.html')
    
def details(request, id):
    item = Tickers.objects.get(id = id)
    topics = Topic.objects.filter(parent_ticker = item)
    try:
        code = (f'{item.nseCode}.NS')
        msft = yf.Ticker(code)
        stock = msft.fast_info
        lastPrice = round(stock.last_price,2)
        dayLow = round(stock.day_low, 2 ) 
        dayHigh = round(stock.day_high,2)
        markCap = round(stock.market_cap/10000000,2)
        openPrice = round(stock.open,2)
        prevClose = round(stock.previous_close,2)
        volume = round(stock.last_volume,2)
    except:
        print('Some Error Occurred in Api call of stock price')

    return render(request, 'home/details.html', {
        'item': item,
        'topics': topics,
        'lastPrice' : lastPrice,
        'dayLow': dayLow,
        'dayHigh': dayHigh,
        'volume': volume,
        'markCap': markCap,
        'openPrice': openPrice,
        'prevClose': prevClose
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

def search(request):
    if request.method == 'POST':
        text = request.POST['search_term'].strip()
        results = list(Tickers.objects.filter(title__icontains = text))
        tickers = Get_All_Tickers()
        return render(request, 'home/index.html',
        {
            'search_results': results,
            'tickers': tickers
        })
    return redirect('home')

def data(request):
    Tickers.objects.all().delete()
    csv_file_path = os.path.abspath('home/nse.csv')
    with open(csv_file_path, 'r',newline='') as file:
        stocks = csv.DictReader(file)
     
        for stock in stocks:
            ticker = Tickers(
                title = stock['NAME OF COMPANY'],
                nseCode = stock['SYMBOL']
            )
            ticker.save()        
    return HttpResponse('bhenchod..11')

def watch(request, id):
    stock = Tickers.objects.get(id = id)
    user = User.objects.get(id = request.user.id)
    return HttpResponse('done') 
#redirect(f'/share/{id}', added = True)
