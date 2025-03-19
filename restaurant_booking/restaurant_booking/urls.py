from django.contrib import admin
from django.urls import path, include
from booking.views import home
from booking import views  # Corrected here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('booking.urls')),
    path('', home, name='home'),
    path('tables/', views.table_status, name='table_status'),  # Now works!
]
