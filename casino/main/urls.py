from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.register_page, name='register_page'),
    path('home/', views.home, name='home'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('deposit_eth/', views.deposit_eth, name='deposit_eth'),
    path('withdraw_eth/', views.withdraw_eth, name='withdraw_eth'),
]
