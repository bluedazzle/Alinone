from django.db import models

# Create your models here.
class PhoneVerify(models.Model):
    phone = models.CharField(max_length=11)
    verify_code = models.CharField(max_length=15, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.phone
