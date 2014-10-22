from CronOrder.models import Merchant


class MyCustomBackend:

    def authenticate(self, Alin_account=None, password=None):
        try:
            user = Merchant.objects.get(alin_account=Alin_account)
        except Merchant.DoesNotExist:
            pass
        else:
            if user.check_password(password):
                return user
        return false

    def get_user(self, user_id):
        try:
            return Merchant.objects.get(pk=user_id)
        except Merchant.DoesNotExist:
            return None
