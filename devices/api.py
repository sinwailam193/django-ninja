from django.shortcuts import get_object_or_404
from ninja_extra import NinjaExtraAPI, api_controller, route, permissions, throttle

from .models import Device, Location
from .schemas import (
    DeviceSchema,
    LocationSchema,
    DeviceCreateSchema,
    Error,
    DeviceLocationUpdate,
)

api = NinjaExtraAPI()


@api_controller(
    "/devices", tags=["Devices"], permissions=[permissions.IsAuthenticatedOrReadOnly]
)
class DeviceController:
    @route.get("", response=list[DeviceSchema])
    @throttle
    def get_devices(self):
        return Device.objects.all()

    @route.get("/{slug}", response=DeviceSchema)
    def get_device(self, slug: str):
        device = get_object_or_404(Device, slug=slug)

        return device

    @route.post("", response={200: DeviceSchema, 404: Error})
    def create_device(self, device_fields: DeviceCreateSchema):
        if device_fields.location_id is not None:
            location_exits = Location.objects.filter(
                id=device_fields.location_id
            ).exists()
            if not location_exits:
                return 404, {"detail": "Location not found"}

        device_data = device_fields.model_dump()
        device_model = Device.objects.create(**device_data)

        return device_model

    @route.put("/{slug}/set-location", response=DeviceSchema)
    def update_device_location(self, slug: str, location: DeviceLocationUpdate):
        device = get_object_or_404(Device, slug=slug)
        if location.location_id is not None:
            location = get_object_or_404(Location, id=location.location_id)
            device.location = location
        else:
            device.location = None

        device.save()
        return device


@api_controller("/locations", tags=["Locations"], permissions=[])
class LocationController:
    @route.get("", response=list[LocationSchema], tags=["Locations"])
    def get_locations(self):
        return Location.objects.all()


api.register_controllers(DeviceController, LocationController)
