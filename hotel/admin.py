from django.contrib import admin
from .models import Room, Reservation

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type', 'price_per_night', 'photo', 'quantity', 'description')  # Fotoğrafı ve açıklamayı listeye ekleyin
    fields = ('name', 'room_type', 'description', 'price_per_night', 'photo', 'quantity')  # Fotoğrafı ve oda sayısını düzenleme formuna ekleyin
    list_editable = ('quantity',)  # Oda sayısını düzenlenebilir yapın

admin.site.register(Room, RoomAdmin)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'guests', 'Ozel_istek')  # Rezervasyon detaylarını listeye ekleyin
