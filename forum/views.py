from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect



def welcome(request):
    return HttpResponse('hello, welcome to the forum')