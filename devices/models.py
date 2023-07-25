from django.db import models
import uuid 

LIGHT = 'Light'
FAN = 'Fan'
PLUG = 'Plug'
CATEGORY_CHOICES = (
    (LIGHT, 'Light'),
    (FAN, 'Fan'),
    (PLUG, 'Plug'),
)



class Device(models.Model):
    device_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField( max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.device_id