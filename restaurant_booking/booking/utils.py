from django.core.mail import send_mail

def send_confirmation_email(reservation):
    subject = "Table Reservation Confirmation"
    message = f"""
    Dear {reservation.customer.name},

    Your reservation is confirmed!
    - Date: {reservation.date}
    - Time: {reservation.time}
    - Guests: {reservation.guests}
    - Table Number: {reservation.table.table_number}

    Thank you for choosing our restaurant!
    """
    send_mail(subject, message, 'noreply@restaurant.com', [reservation.customer.email])
