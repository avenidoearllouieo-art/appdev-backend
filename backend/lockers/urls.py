from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    
    # Locker endpoints
    path('lockers/', views.lockers_list, name='lockers_list'),
    path('lockers/<int:id>/', views.locker_detail, name='locker_detail'),
    path('lockers/<int:id>/rent/', views.rent_locker, name='rent_locker'),
    path('lockers/<int:id>/release/', views.release_locker, name='release_locker'),
]