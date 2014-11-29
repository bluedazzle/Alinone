from django.db import models
from CronOrder.models import *

# Create your models here.
class Proxy(models.Model):
    ip = models.CharField(max_length=30)
    bind_merchant = models.ForeignKey(Merchant, null=True, blank=True)
    get_time = models.DateTimeField(max_length=30)
    is_used = models.BooleanField(default=False)
    req_times = models.IntegerField(default=0, max_length=2)
    is_online = models.BooleanField(default=False)

    def __unicode__(self):
        return self.ip