from django.contrib import admin
from .models import Room, Reservation

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_night', 'photo')  # Fotoğrafı listeye ekleyin
    fields = ('name', 'description', 'price_per_night', 'photo')  # Fotoğrafı düzenleme formuna ekleyin

admin.site.register(Room, RoomAdmin)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'guests', 'Ozel_istek')