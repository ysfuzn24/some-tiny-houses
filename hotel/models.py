from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

class Room(models.Model):
    ROOM_TYPES = [
        ('Deluxe', 'Deluxe Bahceli Oda'),
        ('Standard', 'Standart Oda'),
        ('Suite', 'Suite Oda'),
        ('Deluxe cift', 'Deluxe Bahceli Cift Kisilik Oda'),
        ('Standard cift ', 'Standart Cift Kisilik Oda'),
    ]

    name = models.CharField(max_length=100)
    room_type = models.CharField(choices=ROOM_TYPES, max_length=50)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    photo = models.ImageField(upload_to='room_photos/', blank=True, null=True)  # Fotoğraf alanı eklendi
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1) #Oda sayısı
    def is_available(self, check_in, check_out):
        overlapping_reservations = Reservation.objects.filter(
            room=self,
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).count()
        return overlapping_reservations < self.quantity  # Oda sayısını kontrol et

    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()
    Ozel_istek = models.TextField(null=True, blank=True)

    def clean(self):
        if self.check_out <= self.check_in:
            raise ValidationError("Çıkış tarihi, giriş tarihinden sonra olmalıdır.")

    def clean(self):
        # Oda müsaitliğini kontrol et
        if not self.room.is_available(self.check_in, self.check_out):
            raise ValidationError(f"Seçtiğiniz tarihlerde {self.room.name} odasından boş yer kalmamıştır.")

    def __str__(self):
        return f"Reservation by {self.user.username} for {self.room.name}"