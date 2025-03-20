from django.contrib import admin
from django.urls import path, include
from booking.views import home
from booking import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('booking.urls')),
    path('', views.user_login, name='login'),
    path('index/', views.index, name='index'), 
    path('tables/', views.table_status, name='table_status'),
    path('logout/', views.user_logout, name='logout'),  
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('cancel-booking/<int:reservation_id>/', views.cancel_booking, name='cancel_booking'),
    path('review/<int:reservation_id>/', views.submit_review, name='submit_review'),

]
