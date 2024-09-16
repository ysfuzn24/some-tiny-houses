from django.db import models
from django.contrib.auth.models import User
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
    availability = models.BooleanField(default=True) #Tarihlere göre müsaitlik durumu görüntülenecek şekilde düzeltilecek
    description = models.TextField()

    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()
    Ozel_istek = models.TextField()

    def __str__(self):
        return f"Reservation by {self.user.username} for {self.room.name}"
