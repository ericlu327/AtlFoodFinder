from django.contrib import admin
<<<<<<< HEAD
from django.contrib.auth import views as auth_views
from django.urls import include, path
=======
from django.urls import path, include
from django.urls import path
from places import views
>>>>>>> testFavorite

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('places.urls')),
<<<<<<< HEAD
    path('accounts/', include('django.contrib.auth.urls')),  # Handles login/logout

    # Logout redirect
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Login URL
    path('login/', auth_views.LoginView.as_view(), name='login'),
=======
    path('accounts/', include('django.contrib.auth.urls')),
    path('add-to-favorite/', views.add_to_favorite, name='add_to_favorite'), #added favorite
>>>>>>> testFavorite
]

