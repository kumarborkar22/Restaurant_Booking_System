from django.contrib import admin
from .models import Customer, Table, Reservation, Review

admin.site.register(Customer)
admin.site.register(Table)
admin.site.register(Reservation)
admin.site.register(Review)