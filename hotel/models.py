from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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

    def is_available(self, check_in, check_out):
        # Bu oda için belirtilen tarih aralığında yapılan rezervasyonları al
        overlapping_reservations = Reservation.objects.filter(
            room=self,
            check_in__lt=check_out,  # Çıkış tarihinden önce giriş yapılmış
            check_out__gt=check_in   # Giriş tarihinden sonra çıkış yapılmış
        )

        # Mevcut rezervasyonların sayısını al
        reserved_rooms = overlapping_reservations.count()
        # Kalan oda sayısını dön
        return self.quantity - reserved_rooms

    def __str__(self):
        return self.name


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()
    special_requests = models.TextField(null=True, blank=True)

    def clean(self):
        if self.check_out <= self.check_in:
            raise ValidationError("Çıkış tarihi, giriş tarihinden sonra olmalıdır.")

        # Odanın uygun olup olmadığını kontrol et
    def save(self, *args, **kwargs):

        self.clean()

        if not self.pk:  # Yeni rezervasyon
            self.room.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.room.room_type} rezervasyonu ({self.check_in} - {self.check_out})"


class ContactInfo(models.Model):
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    location_lat = models.FloatField(blank=True, null=True)
    location_lng = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Contact Info - {self.email}"
