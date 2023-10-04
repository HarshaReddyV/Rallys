from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('under', views.under, name='under'),
    path('signin', views.signin,name='signin'),
    path('signup/', views.signup,name='signup'),
    path('profile', views.profile, name='profile'),
    path('signout', views.signout, name='signout'),
    path('share/<int:id>', views.details, name ='details'),
    path('register', views.register, name='register')
]