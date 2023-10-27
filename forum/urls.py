from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('add/<int:id>', views.add, name='add'),
    path('topic/<int:id>', views.topic, name="topic")
]