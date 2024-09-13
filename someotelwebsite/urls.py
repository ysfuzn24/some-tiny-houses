from django.contrib import admin
from django.urls import path, include
from hotel.views import room_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hotel.urls')),
]
