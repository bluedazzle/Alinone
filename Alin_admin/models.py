from django.db import models
from django import forms
import hashlib
import datetime


class AlinAdmin(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=40)
    create_date = models.DateTimeField(auto_created=True)
    last_login_date = models.DateTimeField(null=True, blank=True)

    def hashed_password(self, password=None):
        if not password:
            return self.password
        else:
            return hashlib.md5(password).hexdigest()

    def check_password(self, password):
        if self.hashed_password(password) == self.password:
            self.last_login_date = datetime.datetime.utcnow()
            self.save()
            return True
        return False

    def update_login_date(self):
        self.last_login_date = datetime.datetime.utcnow()
        self.save()

    def __unicode__(self):
        return self.username


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=40)

    def check_valid(self):
        if not self.is_valid():
            return False
        print self.cleaned_data['username']
        print self.cleaned_data['password']
        user_admin = AlinAdmin.objects.filter(username=self.cleaned_data['username'])
        if user_admin.count() == 0:
            return False
        print user_admin.first().username
        return user_admin.first().check_password(self.cleaned_data['password'])