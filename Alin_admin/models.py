from django.db import models


class AlinAdmin(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    create_date = models.DateTimeField()

    def hashed_password(self, password=None):
        if not password:
            return self.password
        else:
            return hashlib.md5(password).hexdigest()

    def check_password(self, password):
        if self.hashed_password(password) == self.password:
            return True
        return False