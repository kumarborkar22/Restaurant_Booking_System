from django.contrib import admin
from django.urls import path, include
from booking.views import home
from booking import views  # ✅ Import views properly

urlpatterns = [
    path('admin/', admin.site.urls),  # ✅ Admin panel
    path('api/', include('booking.urls')),  # ✅ Include API routes
    path('', views.user_login, name='login'),  # ✅ Default to login page
    path('index/', views.index, name='index'),  # ✅ Redirect to index after login
    path('tables/', views.table_status, name='table_status'),  # ✅ Table status page
    path('logout/', views.user_logout, name='logout'),  # ✅ Logout route
]
