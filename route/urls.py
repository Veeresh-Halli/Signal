from django.urls import path
from . import views


urlpatterns = [
    path('', views.index ,name='index'),
    path('register/', views.register,name='register'),
    path('loginpage/', views.LoginPage ,name='loginpage'),
    path('logoutpage/', views.LogoutPage ,name='logoutpage'),
    path('dashboard/', views.dashboard ,name='dashboard'),
    path('users/', views.UsersPage,name='users'),

    
]