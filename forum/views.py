from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from .models import Topic, Comment
from home.models import Tickers
from .forms import CommentForm
from django.contrib.auth.decorators import login_required


from django.shortcuts import redirect

def go_back(request):
    # Get the HTTP_REFERER from the request's META information
    previous_page = request.META.get('HTTP_REFERER')
    
    if previous_page:
        # If the HTTP_REFERER is available, redirect to it
        return redirect(previous_page)
    else:
        # If there's no previous page, redirect to a default URL or handle it accordingly
        return redirect('your_default_url_name')



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


@login_required(login_url='signin')
def topic(request, id):
    topic = Topic.objects.get(id = id)
    form = CommentForm()
    return render(request, 'forum/topic.html', {
        'topic': topic,
        'form': form
        })

@login_required(login_url='signin')
def comment(request, id):
    topic = Topic.objects.get(id = id)
    form = CommentForm(request.POST)
    if form.is_valid():
        text= form.cleaned_data['text']
        comment = Comment(
        user = request.user,
        topic = topic,
        text = text)
        Comment.save(comment)
        print('comment saved')
        return go_back(request)
    else:
        return go_back(request)
    
    