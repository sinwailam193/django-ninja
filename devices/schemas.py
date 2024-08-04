from ninja import ModelSchema, Schema

from .models import Device, Location


class LocationSchema(ModelSchema):
    class Meta:
        model = Location
        fields = ("id", "name")


class DeviceSchema(ModelSchema):
    # since location is a foreign key
    location: LocationSchema | None = None

    class Meta:
        model = Device
        fields = ("id", "name", "location")


class DeviceCreateSchema(Schema):
    name: str
    location_id: int | None = None


class DeviceLocationUpdate(Schema):
    location_id: int | None = None


class Error(Schema):
    detail: str
