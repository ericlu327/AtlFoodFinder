# foodfinder/places/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('place/<int:pk>/', views.food_place_detail, name='food_place_detail'),
    path('place/<int:pk>/add_review/', views.add_review, name='add_review'),
    path('signup/', views.signup, name='signup'),
]
