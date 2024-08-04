from django.shortcuts import get_object_or_404
from ninja import NinjaAPI

from .models import Device, Location
from .schemas import (
    DeviceSchema,
    LocationSchema,
    DeviceCreateSchema,
    Error,
    DeviceLocationUpdate,
)

api = NinjaAPI()


@api.get("devices/", response=list[DeviceSchema])
def get_devices(request):
    return Device.objects.all()


@api.get("devices/{slug}/", response=DeviceSchema)
def get_device(request, slug: str):
    device = get_object_or_404(Device, slug=slug)

    return device


@api.post("devices/", response={200: DeviceSchema, 404: Error})
def create_device(request, device_fields: DeviceCreateSchema):
    if device_fields.location_id is not None:
        location_exits = Location.objects.filter(id=device_fields.location_id).exists()
        if not location_exits:
            return 404, {"detail": "Location not found"}

    device_data = device_fields.model_dump()
    device_model = Device.objects.create(**device_data)

    return device_model


@api.get("locations/", response=list[LocationSchema])
def get_devices(request):
    return Location.objects.all()


@api.put("devices/{slug}/set-location/", response=DeviceSchema)
def update_device_location(request, slug: str, location: DeviceLocationUpdate):
    device = get_object_or_404(Device, slug=slug)
    if location.location_id is not None:
        location = get_object_or_404(Location, id=location.location_id)
        device.location = location
    else:
        device.location = None

    device.save()
    return device
