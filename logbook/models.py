
from django.db import models
from django.utils.translation import gettext_lazy as _

class Userlog (models.Model):

    user = models.CharField(max_length=200, blank=True, null=True)
    last_activity = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP')
    last_activation_date = models.DateTimeField()

    def __str__(self):
        return self.user