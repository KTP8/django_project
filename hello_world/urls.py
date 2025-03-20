from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('booking/', views.booking, name='booking_page'),
    
    # Reservation management URLs for owners:
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('reservations/<int:pk>/delete/', views.reservation_delete, name='reservation_delete'),
]
