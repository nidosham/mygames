from . import views
from django.urls import path, include
urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.index, name='index'),
    path('createpost', views.createpost, name='createpost'),
    path('editpost', views.editpost, name='editpost'),
    path('about', views.about, name='about'),
    path('mymessages', views.mymessages, name='mymessages'),
    path('mymessages/<int:id>/', views.myinbox, name='myinbox'),
    path('contactus', views.contactus, name='contactus'),
    path('playerhome/', views.playerhome, name='playerhome'),
    path('playerhome/searchresults/',
         views.searchresults, name='searchresults'),
    path('register', views.registration, name='registration'),
    path('settings/', views.settings, name='settings'),
    path('playerhome/mygames/', views.mygames, name='mygames'),
    #path('post/<int:id>/message/', views.post_message, name='post_message'),
    path(
        'post/<int:id>/', views.postDetail, name='postDetail'),
    path(
        'games/<int:id>/', views.gameDetail, name='gameDetail'),
    path('profile/', views.profile, name='profile'),
    path('myposts/', views.myposts, name='myposts'),
    path('faqs/', views.faqs, name='faqs'),
    path('logout/', views.logout, name='logout'),

]
