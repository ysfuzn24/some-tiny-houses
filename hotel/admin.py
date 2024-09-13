from django.contrib import admin
from .models import Room

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_night', 'photo')  # Fotoğrafı listeye ekleyin
    fields = ('name', 'description', 'price_per_night', 'photo')  # Fotoğrafı düzenleme formuna ekleyin

admin.site.register(Room, RoomAdmin)