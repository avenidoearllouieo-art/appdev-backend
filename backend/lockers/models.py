from django.db import models

class Locker(models.Model):
    number = models.IntegerField()
    status = models.CharField(max_length=20, default="Available")
    time_left = models.IntegerField(default=0)

    def __str__(self):
        return f"Locker {self.number} - {self.status}"