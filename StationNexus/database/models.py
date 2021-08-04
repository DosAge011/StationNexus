from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Station(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    number = models.IntegerField()
    is_active = models.BooleanField(default=False)

    def as_json(self):
        return dict(name=self.name, number=self.number)


class Unit(models.Model):

    call_sign = models.CharField(max_length=10)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    unit_type = models.CharField(max_length=5)
    status = models.CharField(max_length=5)
    event_id = models.CharField(max_length=10, null=True)
    event_type = models.CharField(max_length=10, null=True)
    event_sub_type = models.CharField(max_length=10, null=True)
    location = models.CharField(max_length=30, null=True)
    unit_phone_number = models.CharField(max_length=10, null=True)
    employee_one = models.CharField(max_length=30, null=True)
    employee_two = models.CharField(max_length=30, null=True)
    last_status_change = models.DateTimeField(auto_now=True)

    out_of_service_code = models.CharField(max_length=10, null=True, blank=True)


class Broadcast_Message(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    display_time = models.IntegerField()
    image = models.ImageField(upload_to="images/")
    image_sized = ImageSpecField(
        source="image",
        processors=[ResizeToFill(800, 800)],
        format="JPEG",
        options={"quality": 60},
    )
