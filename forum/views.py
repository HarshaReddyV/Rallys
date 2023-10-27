from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from .models import Topic, Comment
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def add(request, id):
    if request.method == 'GET':
        return render(request, 'forum/add.html', {'id': id})
    elif request.method == 'POST':
        return redirect(f'/share/{id}')

