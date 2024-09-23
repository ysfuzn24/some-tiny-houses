from django.contrib import admin
from .models import Room, Reservation, ContactInfo
from django.core.exceptions import ValidationError


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type', 'price_per_night', 'photo', 'quantity', 'description')  # Fotoğrafı ve açıklamayı listeye ekleyin
    fields = ('name', 'room_type', 'description', 'price_per_night', 'photo', 'quantity')  # Fotoğrafı ve oda sayısını düzenleme formuna ekleyin
    list_editable = ('quantity',)  # Oda sayısını düzenlenebilir yapın

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

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'guests', 'special_requests')  # Rezervasyon detaylarını listeye ekleyin

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'address')
    fields = ('email', 'phone_number', 'address')
