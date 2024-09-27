from django.contrib import admin
from .models import Room, ContactInfo
from django.core.exceptions import ValidationError
from reservations.models import Reservation


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type', 'price_per_night', 'photo', 'quantity', 'description','max_occupancy')  # Fotoğrafı ve açıklamayı listeye ekleyin
    fields = ('name', 'room_type', 'description', 'price_per_night', 'photo', 'quantity', 'max_occupancy')  # Fotoğrafı ve oda sayısını düzenleme formuna ekleyin
    list_editable = ('quantity', 'max_occupancy')  # Oda sayısını düzenlenebilir yapın

    def save_model(self, request, obj, form, change):
        if change:  # Mevcut bir oda güncelleniyorsa
            original_obj = Room.objects.get(pk=obj.pk)
            if obj.quantity < original_obj.quantity:
            # Rezervasyon kontrolü yap
                existing_reservations = Reservation.objects.filter(room=obj).count()

                if existing_reservations > obj.quantity:
                    raise ValidationError( f"Bu oda için mevcut rezervasyon sayısı {existing_reservations}, yeni oda sayısından ({obj.quantity}) fazla.")
            # Eğer mevcut rezervasyonlar yeni quantity'den fazlaysa hata ver
        super().save_model(request, obj, form, change)

admin.site.register(Room, RoomAdmin)

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'address')
    fields = ('email', 'phone_number', 'address')
