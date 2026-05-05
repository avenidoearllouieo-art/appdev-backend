from django.urls import path
from . import views

urlpatterns = [
    path('lockers/', views.get_lockers),
    path('lockers/<int:id>/open/', views.open_locker),
    path('lockers/<int:id>/', views.delete_locker),
    path('register/', views.register_user),
    path('login/', views.login_user),
]