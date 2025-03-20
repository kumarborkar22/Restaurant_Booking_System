from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.table_number} (Capacity: {self.capacity})"


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    cancel_status = models.BooleanField(default=False)  # ✅ Track canceled status
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"Reservation by {self.customer.name} on {self.date} at {self.time}"

class Review(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)  # Rating 1 to 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Table {self.reservation.table.table_number}"