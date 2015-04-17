from django.db import models

# Create your models here.
class PhoneVerify(models.Model):
    phone = models.CharField(max_length=11)
    verify_code = models.CharField(max_length=15, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.phone


class ApiTimes(models.Model):
    ip = models.CharField(max_length=15, unique=True)
    req_times = models.IntegerField(default=0)
    last_req_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.ip
