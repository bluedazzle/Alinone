from django.db import models
from CronOrder.models import Merchant


class Notice(models.Model):
    content = models.CharField(max_length=100, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content


class FeedBack(models.Model):
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    merchant = models.ForeignKey(Merchant, related_name='feedback')

    def __unicode__(self):
        return self.merchant.name