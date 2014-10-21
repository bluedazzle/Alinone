from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import hashlib
# Create your models here.

class MerchantManager(BaseUserManager):

    def create_user(self, email, alin_account, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email = MerchantManager.normalize_email(email),
            username = alin_account,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, alin_account, password):

        user = self.create_user(email,
            username = alin_account,
            password = password,

        )
        user.is_staff = True
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class Merchant(AbstractBaseUser):
    name = models.CharField(max_length=50)
    alin_account = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=254, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    tao_account = models.CharField(max_length=15, blank=True)
    tao_passwd = models.CharField(max_length=50, blank=True)
    mei_account = models.CharField(max_length=15, blank=True)
    mei_passwd = models.CharField(max_length=50, blank=True)
    ele_account = models.CharField(max_length=15, blank=True)
    ele_passwd = models.CharField(max_length=50, blank=True)

    is_online = models.BooleanField(default=True)
    is_open = models.BooleanField(default=False)

    USERNAME_FIELD = 'alin_account'
    REQUIRED_FIELDS = ['alin_account']
    objects = MerchantManager()

    def __unicode__(self):
        return self.alin_account

    def is_authenticated(self):
        return True

    def hashed_password(self, password=None):
        if not password:
            return self.password
        else:
            return hashlib.md5(password).hexdigest()

    def check_password(self, password):
        if self.hashed_password(password) == self.password:
            return True
        return False

    class Meta:
        app_label = 'CronOrder'


class DayOrder(models.Model):
    order_id_alin = models.CharField(max_length=20, unique=True)
    order_id_old = models.CharField(max_length=20)
    order_time = models.DateTimeField(max_length=30)
    send_time = models.DateTimeField(max_length=30)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=50)
    platform = models.IntegerField(max_length=1)
    origin_price = models.FloatField(max_length=10)
    promotion = models.CharField(max_length=50)
    real_price = models.FloatField(max_length=10)
    status = models.IntegerField(max_length=1)
    merchant = models.ForeignKey(Merchant, blank=True, null=True)


    def __unicode__(self):
        return self.order_id_alin

class Dish(models.Model):
    dish_name = models.CharField(max_length=30)
    dish_price = models.FloatField(max_length=5)
    dish_count = models.IntegerField(max_length=5)
    order = models.ForeignKey(DayOrder, blank=True, null=True)

    def __unicode__(self):
        return  self.dish_name

class Sender(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    passwd = models.CharField(max_length=50)
    bind_order = models.ManyToManyField(DayOrder, blank=True, null=True)
    lng = models.FloatField(max_length=10, blank=True, null=True)
    lat = models.FloatField(max_length=10, blank=True, null=True)
    update_time = models.DateTimeField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return  self.phone

class abc(models.Model):
    usrid = models.IntegerField(default=1)
    i = models.IntegerField(default=1)
    ison = models.IntegerField(default=1)

    def __unicode__(self):
        return str(self.usrid)