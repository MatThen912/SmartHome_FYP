from django.db import models

LIGHT = 'Light'
FAN = 'Fan'
PLUG = 'Plug'
CATEGORY_CHOICES = (
    (LIGHT, 'Light'),
    (FAN, 'Fan'),
    (PLUG, 'Plug'),
)

class Device(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name