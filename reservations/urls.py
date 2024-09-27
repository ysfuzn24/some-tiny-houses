from django.urls import path
from . import views

urlpatterns = [
    path('room_search/', views.room_search_view, name='room_search'),
    path('reservation/<int:room_id>/', views.reservation_view, name='reservation'),
    path('reservation/success/', views.reservation_success_view, name='reservation_success'),
]