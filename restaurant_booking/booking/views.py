from rest_framework import generics, status
from rest_framework.response import Response
from .models import Customer, Table, Reservation
from .serializers import CustomerSerializer, TableSerializer, ReservationSerializer
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
import json


# ✅ Home View for Rendering Homepage
def home(request):
    return render(request, 'booking/index.html')


# ✅ Utility: Send Confirmation Email
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


# ✅ Customer CRUD API with Duplicate Email Check
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        """Handle duplicate customer creation gracefully"""
        try:
            print("🔍 Incoming Customer Data: ", json.dumps(request.data, indent=4))
            
            # Get customer data from request
            email = request.data.get("email")

            # Check if customer with email already exists
            if Customer.objects.filter(email=email).exists():
                existing_customer = Customer.objects.get(email=email)
                return Response(
                    {"id": existing_customer.id, "message": "Customer already exists."},
                    status=status.HTTP_200_OK,
                )
            
            # If customer does not exist, create a new one
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


# ✅ Table CRUD API
class TableListCreateView(generics.ListCreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class TableDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


# ✅ Reservation CRUD API
# views.py
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

            # ✅ Check if the table is available for the selected date and time
            if Reservation.objects.filter(table_id=table_id, date=date, time=time).exists():
                return Response(
                    {"error": "The selected table is already reserved for this time."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Proceed with creating the reservation
            response = super().create(request, *args, **kwargs)

            # Send confirmation email after successful reservation
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
