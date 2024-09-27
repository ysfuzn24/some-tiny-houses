from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    ROOM_TYPES = [
        ('Deluxe', 'Deluxe Bahçeli Oda'),
        ('Standard', 'Standart Oda'),
        ('Suite', 'Suite Oda'),
        ('Deluxe cift', 'Deluxe Bahçeli Çift Kişilik Oda'),
        ('Standard cift', 'Standart Çift Kişilik Oda'),
    ]

    name = models.CharField(max_length=100)
    room_type = models.CharField(choices=ROOM_TYPES, max_length=50)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    photo = models.ImageField(upload_to='room_photos/', blank=True, null=True)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)  # Toplam oda sayısı
    max_occupancy=models.PositiveIntegerField(default=1) #maksimum misafir

    def is_available(self, check_in, check_out):
        """
        Odanın belirtilen tarihler arasında uygun olup olmadığını kontrol eder.
        """
        from reservations.models import Reservation
        overlapping_reservations = Reservation.objects.filter(
            room=self,
            check_in__lt=check_out,  # Çıkış tarihi giriş tarihinden sonra olmalı
            check_out__gt=check_in  # Giriş tarihi çıkış tarihinden önce olmalı
        )
        reserved_rooms = overlapping_reservations.count()

        # Eğer oda sayısından fazla rezervasyon yapılmışsa oda mevcut değildir.
        return self.quantity > reserved_rooms

class ContactInfo(models.Model):
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    location_lat = models.FloatField(blank=True, null=True)
    location_lng = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Contact Info - {self.email}"
