from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('requested', 'Requested'),
    ]

    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='items')
    rental_price = models.IntegerField()
    description = models.TextField()
    keywords = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_items')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.name
    

class RentalRequest(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('rented', 'Rented'),
        ('returned', 'Returned')
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='rental_requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rental_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='requested')
    requested_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.item.name} requested by {self.requester.username}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username