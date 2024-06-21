from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Room(models.Model):
    room_number = models.IntegerField()
    room_type = models.CharField(max_length=10)
    price_per_night = models.IntegerField()
    description = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return f"{self.room_number} - {self.room_type} - {self.price_per_night}"
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    def __str__(self):
        return f"{self.room} - {self.check_in} - {self.check_out}"

