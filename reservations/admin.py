from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'guests', 'special_requests')
    search_fields = ('user__username', 'room__room_type')  # Kullanıcı adı veya oda tipi ile arama
    list_filter = ('check_in', 'check_out', 'guests')  # Giriş ve çıkış tarihleri ile filtreleme
