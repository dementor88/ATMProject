import datetime

from django.db import models
from django.conf import settings

# Create your models here.
# TODO: in case we need to store and query bank info
class Bank(models.Model):
    bank_name = models.CharField(max_length=100)
    bank_code = models.CharField(unique=True, max_length=100)
    bank_info = models.JSONField()  # may include additional extra info

    def get(self, bank_code):
        try:
            return Bank.objects.get(bank_code=bank_code)
        except Bank.DoesNotExist:
            return None

    def add(self, bank_code, bank_name, bank_info):
        bank = Bank.objects.create(bank_name=bank_name, bank_code=bank_code, bank_info=bank_info)
        return bank.id

TOKEN_LIFE = settings.TOKEN_LIFE # seconds
class BankCheckToken(models.Model):
    card_number = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    expires = models.DateTimeField()

    def add(self, card_number, token):
        BankCheckToken.objects.create(card_number=card_number, token=token, expires=datetime.datetime.now() + datetime.timedelta(0,TOKEN_LIFE))

    def check_token(self, card_number, token):
        try:
            token = BankCheckToken.objects.get(card_number=card_number, token=token)
            if token.expires > datetime.datetime.now():
                return True
            return False
        except BankCheckToken.DoesNotExist:
            return False

    def remove_token(self, card_number, token):
        token = BankCheckToken.objects.get(card_number=card_number, token=token)
        token.delete()