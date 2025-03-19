from django.urls import path
from .views import (
    CustomerListCreateView,
    CustomerDetailView,
    TableListCreateView,
    TableDetailView,
    ReservationListCreateView,
    ReservationDetailView,
)

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('tables/', TableListCreateView.as_view(), name='table-list-create'),
    path('tables/<int:pk>/', TableDetailView.as_view(), name='table-detail'),
    path('reservations/', ReservationListCreateView.as_view(), name='reservation-list-create'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),
]
