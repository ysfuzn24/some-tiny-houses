from django.urls import path
from .views import room_list, index

urlpatterns = [
    path('', index, name='index'),
    path('rooms/', room_list, name='room_list'),
]