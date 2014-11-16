from django.db import models

class CronLog(models.Model):
    ltype = models.IntegerField(max_length=2)
    content = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    log_time = models.DateTimeField(max_length=30, auto_now_add=True)
    err_message = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.content

