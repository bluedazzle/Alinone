from django.db import models
from CronOrder.models import *

class CronLog(models.Model):
    ltype = models.IntegerField(max_length=2)
    content = models.CharField(max_length=500)
    status = models.BooleanField(default=True)
    log_time = models.DateTimeField(max_length=30, auto_now_add=True)
    err_message = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.content

class RunTimeLog(models.Model):
    merchant = models.ForeignKey(Merchant, null=True, blank=True)
    ltype = models.IntegerField(max_length=2)
    content = models.CharField(max_length=500)
    status = models.BooleanField(default=True)
    log_time = models.DateTimeField(auto_now_add=True)
    err_message = models.CharField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return self.content
class AccountLog(models.Model):
    account = models.CharField(max_length=40, null=True, blank=True)
    atype = models.CharField(max_length=5, default='0')
    ltype = models.IntegerField(max_length=2, default=0)
    content = models.CharField(max_length=500, null=True, blank=True)
    note = models.CharField(max_length=50, null=True, blank=True)
    log_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.account

class SeachLog(models.Model):
    req_ip = models.CharField(max_length=15)
    req_time = models.DateTimeField(auto_now_add=True)
    req_param = models.CharField(max_length=500)

    def __unicode__(self):
        return self.req_ip


