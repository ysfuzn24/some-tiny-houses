from django.db import models
from hotel.models import Room
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField()
    special_requests = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-check_in']

    def clean(self):
        if not self.check_in or not self.check_out:
            raise ValidationError("Giriş ve çıkış tarihleri belirtilmelidir.")
        if self.check_in < timezone.now().date():
            raise ValidationError("Giriş tarihi geçmiş bir tarih olamaz.")
        if self.check_out <= self.check_in:
            raise ValidationError("Çıkış tarihi, giriş tarihinden sonra olmalıdır.")
        if (self.check_out - self.check_in).days > 30:
            raise ValidationError("Rezervasyon süresi 30 günü aşamaz.")
        if self.guests > self.room.max_occupancy:
            raise ValidationError(f"Misafir sayısı oda kapasitesini ({self.room.max_occupancy}) aşıyor.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def is_available(cls, room, check_in, check_out):
        overlapping_reservation_count = cls.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in
        ).count()
        return room.quantity > overlapping_reservation_count

    def __str__(self):
        return f"{self.user.username}'in {self.room.room_type} rezervasyonu ({self.check_in} - {self.check_out})"
