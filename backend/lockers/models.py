from django.db import models
from django.contrib.auth.models import User


class Locker(models.Model):
    """
    Smart Locker Model - Lab 9 Requirements
    
    Locker object structure:
    {
      "id": 1,
      "locker_number": 1,
      "status": "Available",
      "rented_by": null,
      "rental_hours": 0,
      "created_at": "2024-01-01T12:00:00Z"
    }
    """
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('In Use', 'In Use'),
    ]
    
    locker_number = models.IntegerField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    rented_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rental_hours = models.IntegerField(default=0)  # rental duration in hours
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['locker_number']

    def __str__(self):
        return f"Locker {self.locker_number} - {self.status}"