from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from places import views as places_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('places.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Handles login/logout
    
    # Logout redirect
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Login URL
    path('login/', auth_views.LoginView.as_view(), name='login'),
    
    # Profile page URL
    path('profile/', places_views.profile, name='profile'),
]