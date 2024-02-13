from django.urls import path
from .import views

urlpatterns =[
    path('register/', views.register, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
]