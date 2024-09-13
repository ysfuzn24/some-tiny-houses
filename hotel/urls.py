from django.urls import path
from .views import room_list, index, signup

urlpatterns = [
    path('', index, name='index'),
    path('rooms/', room_list, name='room_list'),
    path('signup/',signup, name='signup')
]