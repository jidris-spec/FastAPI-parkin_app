from ninja import NinjaAPI
from fastapi_integration.models import ParkingSlot, Booking
from django.contrib.auth.models import User
from datetime import datetime
from ninja import Schema
from .models import ParkingSlot
from django.core.exceptions import ObjectDoesNotExist

api = NinjaAPI()

# Schema for Slot Data
class SlotSchema(Schema):
    slot_number: int
    is_available: bool = True


class SlotUpdateSchema(Schema):
    is_available: bool = None


# Create a new slot
@api.post("/slots/")
def create_slot(request, data: SlotSchema):
    if ParkingSlot.objects.filter(slot_number=data.slot_number).exists():
        return {"error": "A slot with this number already exists"}
    slot = ParkingSlot.objects.create(
        slot_number=data.slot_number,
        is_available=data.is_available
    )
    return {"message": "Slot created successfully", "slot_id": slot.id}


# Retrieve all slots
@api.get("/slots/")
def get_all_slots(request):
    slots = ParkingSlot.objects.all()
    return {
        "slots": [
            {"slot_number": slot.slot_number, "is_available": slot.is_available}
            for slot in slots
        ]
    }


# Retrieve a specific slot
@api.get("/slots/{slot_number}/")
def get_slot(request, slot_number: int):
    try:
        slot = ParkingSlot.objects.get(slot_number=slot_number)
        return {"slot_number": slot.slot_number, "is_available": slot.is_available}
    except ParkingSlot.DoesNotExist:
        return {"error": "Slot not found"}


# Update a slot's availability
@api.put("/slots/{slot_number}/")
def update_slot(request, slot_number: int, data: SlotUpdateSchema):
    try:
        slot = ParkingSlot.objects.get(slot_number=slot_number)
        if data.is_available is not None:
            slot.is_available = data.is_available
            slot.save()
        return {"message": "Slot updated successfully"}
    except ParkingSlot.DoesNotExist:
        return {"error": "Slot not found"}


# Delete a slot
@api.delete("/slots/{slot_number}/")
def delete_slot(request, slot_number: int):
    try:
        slot = ParkingSlot.objects.get(slot_number=slot_number)
        slot.delete()
        return {"message": "Slot deleted successfully"}
    except ParkingSlot.DoesNotExist:
        return {"error": "Slot not found"}






# Schema for user requests
class UserSchema(Schema):
    username: str
    email: str
    first_name: str = None
    last_name: str = None


class UserUpdateSchema(Schema):
    email: str = None
    first_name: str = None
    last_name: str = None


# Create a new user
@api.post("/users/")
def create_user(request, data: UserSchema):
    if User.objects.filter(username=data.username).exists():
        return {"error": "User with this username already exists"}
    user = User.objects.create(
        username=data.username,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name
    )
    return {"message": "User created successfully", "user_id": user.id}

# Retrieve all users
@api.get("/users/") 

def get_all_users(request):
    users = User.objects.all()
    return {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
            for user in users
        ]
    }

# Retrieve user details
@api.get("/users/{user_id}/")
def get_user(request, user_id: int):
    try:
        user = User.objects.get(id=user_id)
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    except ObjectDoesNotExist:
        return {"error": "User not found"}


# Update user details
@api.put("/users/{user_id}/")
def update_user(request, user_id: int, data: UserUpdateSchema):
    try:
        user = User.objects.get(id=user_id)
        if data.email:
            user.email = data.email
        if data.first_name:
            user.first_name = data.first_name
        if data.last_name:
            user.last_name = data.last_name
        user.save()
        return {"message": "User updated successfully"}
    except ObjectDoesNotExist:
        return {"error": "User not found"}


# Delete a user
@api.delete("/users/{user_id}/")
def delete_user(request, user_id: int):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return {"message": "User deleted successfully"}
    except ObjectDoesNotExist:
        return {"error": "User not found"}





class BookingRequest(Schema):
    slot_number: int
    user_id: int
    start_time: datetime
    end_time: datetime


@api.post("/book-slot/")
def book_slot(request, data: BookingRequest):
    try:
        # Get the user and slot
        user = User.objects.get(id=data.user_id)
        slot = ParkingSlot.objects.get(slot_number=data.slot_number)

        if not slot.is_available:
            return {"error": "Slot is already booked"}

        # Create the booking
        booking = Booking.objects.create(
            user=user,
            slot=slot,
            start_time=data.start_time,
            end_time=data.end_time,
        )

        # Mark the slot as unavailable
        slot.is_available = False
        slot.save()

        return {"message": "Booking successful", "booking_id": booking.id}
    except User.DoesNotExist:
        return {"error": "User not found"}
    except ParkingSlot.DoesNotExist:
        return {"error": "Slot not found"}


@api.get("/bookings/")
def get_bookings(request):
    bookings = Booking.objects.all()
    return {"bookings": [
        {
            "user": booking.user.username,
            "slot": booking.slot.slot_number,
            "start_time": booking.start_time,
            "end_time": booking.end_time
        }
        for booking in bookings
    ]}

