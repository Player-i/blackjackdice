from django.urls import path

from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('create/', views.create, name='create'),
    path('<slug:slug>/', views.room, name='room' ),
    path('finish_bet/', views.finish_bet, name='finish_bet'),
    

    
]