from django.urls import path
from . import views

urlpatterns = [
    path('lockers/', views.get_lockers),
    path('lockers/<int:id>/open/', views.open_locker),
]