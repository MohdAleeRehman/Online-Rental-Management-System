from django.contrib import admin
from .models import Item, RentalRequest

# Register your models here.

admin.site.register(Item)
admin.site.register(RentalRequest)
