from django.db import models

# Create your models here.

class Room(models.Model):
    ROOM_TYPES = [
        ('Deluxe', 'Deluxe Bahceli Oda'),
        ('Standard', 'Standart Oda'),
        ('Suite', 'Suite Oda'),
    ]

    name = models.CharField(max_length=100)
    room_type = models.CharField(choices=ROOM_TYPES, max_length=50)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    availability = models.BooleanField(default=True)
    description = models.TextField()

    def __str__(self):
        return self.name
