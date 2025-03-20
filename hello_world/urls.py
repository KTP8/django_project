from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('booking/', views.booking, name='booking_page'),
    path('menu/', views.menu, name='menu_page'),
    path('cancel/<str:token>/', views.cancel_reservation, name='cancel_reservation'),
    # Secure owner reservation views with form-based password entry
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('reservations/<int:pk>/delete/', views.reservation_delete, name='reservation_delete'),
]
