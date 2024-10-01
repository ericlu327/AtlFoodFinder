# foodfinder/foodfinder/urls.py

from django.contrib import admin
from django.urls import path, include
from django.urls import path
from places import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('places.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add-to-favorite/', views.add_to_favorite, name='add_to_favorite'), #added favorite
]
