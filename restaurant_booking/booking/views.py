from rest_framework import generics, status
from rest_framework.response import Response
from .models import Customer, Table, Reservation
from .serializers import CustomerSerializer, TableSerializer, ReservationSerializer
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
import json


def home(request):
    return render(request, 'booking/index.html')


def send_confirmation_email(reservation):
    """Send email confirmation after reservation."""
    subject = "Table Reservation Confirmation"
    message = f"""
    Dear {reservation.customer.name},

    Your reservation has been confirmed!
    - Date: {reservation.date}
    - Time: {reservation.time}
    - Guests: {reservation.guests}
    - Table Number: {reservation.table.table_number}

    Thank you for choosing our restaurant! 🍽️
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [reservation.customer.email],
        fail_silently=False,
    )


class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        """Handle duplicate customer creation gracefully"""
        try:
            print("🔍 Incoming Customer Data: ", json.dumps(request.data, indent=4))
            
            email = request.data.get("email")

            if Customer.objects.filter(email=email).exists():
                existing_customer = Customer.objects.get(email=email)
                return Response(
                    {"id": existing_customer.id, "message": "Customer already exists."},
                    status=status.HTTP_200_OK,
                )
            
            return super().create(request, *args, **kwargs)

        except Exception as e:
            print(f"❌ Error Creating Customer: {e}")
            return Response(
                {"error": "Failed to create customer."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class TableListCreateView(generics.ListCreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class TableDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        """Custom create method to check table availability and send email."""
        try:
            data = request.data
            customer_id = data.get("customer")
            table_id = data.get("table")
            date = data.get("date")
            time = data.get("time")

            if Reservation.objects.filter(table_id=table_id, date=date, time=time).exists():
                return Response(
                    {"error": "The selected table is already reserved for this time."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            response = super().create(request, *args, **kwargs)

            reservation = Reservation.objects.get(id=response.data["id"])
            send_confirmation_email(reservation)

            return response

        except Exception as e:
            print(f"❌ Error Creating Reservation: {e}")
            return Response(
                {"error": "Failed to create reservation."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

from django.shortcuts import render
import json
from datetime import date
from django.http import JsonResponse

# def index(request):
#     return render(request, 'index.html')

def table_status(request):
    # ✅ Get all booked tables (persist even after multiple bookings)
    reservations = Reservation.objects.values_list('table__table_number', flat=True)
    booked_tables = list(set(reservations))
    
    # ✅ Get the last booked table
    last_reservation = Reservation.objects.order_by('-id').first()
    last_booked_table = last_reservation.table.table_number if last_reservation else None

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # ✅ Return JSON for AJAX requests
        return JsonResponse({'booked_tables': booked_tables, 'last_booked_table': last_booked_table})

    # ✅ Pass as JSON string for initial page load
    return render(request, 'booking/tables.html', {
        'booked_tables': json.dumps(booked_tables),
        'last_booked_table': last_booked_table
    })


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# ✅ Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # ✅ Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to index.html after login
        else:
            return render(request, 'booking/login.html', {'error_message': '❌ Invalid Credentials'})

    return render(request, 'booking/login.html')

# ✅ Index Page (Protected)
@login_required
def index(request):
    return render(request, 'booking/index.html')

# ✅ Logout View
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout
