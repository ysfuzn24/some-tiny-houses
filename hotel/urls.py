from django.urls import path
from . import views
from .views import room_list, index, signup

urlpatterns = [
    path('', index, name='index'),
    path('rooms/', room_list, name='room_list'),
    path('signup/',signup, name='signup'),
    path('reservation/<int:room_id>/', views.reservation_view, name='reservation'),
    path('reservation/success/', views.reservation_success_view, name='reservation_success'),
]