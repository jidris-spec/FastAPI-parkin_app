
# Create your models here.

from django.db import models
from django.contrib.auth.models import User
class ParkingSlot(models.Model):
    slot_number = models.IntegerField(unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Slot {self.slot_number} - {'Available' if self.is_available else 'Occupied'}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Booking by {self.user.username} for Slot {self.slot.slot_number} ({self.start_time} - {self.end_time})"
