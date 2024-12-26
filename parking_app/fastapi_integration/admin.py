from django.contrib import admin
from .models import ParkingSlot

@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):
    list_display = ('slot_number', 'is_available')
    list_filter = ('is_available',)

