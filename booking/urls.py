from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('check-availability/', views.check_availability, name='check_availability'),
]
    # urls.py
