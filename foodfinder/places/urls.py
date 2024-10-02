# foodfinder/places/urls.py

from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('', views.index, name='index'),
    path('place/<int:pk>/', views.food_place_detail, name='food_place_detail'),
    path('place/<int:pk>/add_review/', views.add_review, name='add_review'),
    path('signup/', views.signup, name='signup'),
    path('accounts/profile/', lambda request: redirect('index'), name='profile_redirect'),
]
