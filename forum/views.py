from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from .models import Topic, Comment
from home.models import Tickers
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def add(request, id):
    if request.method == 'GET':
        return render(request, 'forum/add.html', {'id': id})
    elif request.method == 'POST':
        topic = request.POST['topic'].strip()
        description = request.POST['description'].strip()
        if topic == '':
            return render(request, 'forum/add.html',{
                'message': "Summary Cannot be empty",
                'id': id})
        
        parent = Tickers.objects.get(id = id)
        item = Topic(
            title = topic,
            description = description,
            parent_ticker = parent,
            author = request.user
        )
        Tickers.save(item)
        return redirect(f'/share/{id}')


def topic(request, id):
    return HttpResponse('This is where the real work goes on...')