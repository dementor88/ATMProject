import datetime

from django.db import models

# Create your models here.
# TODO: in case we need to store and query bank info
class Bank(models.Model):
    bank_name = models.CharField(max_length=120)
    bank_code = models.CharField(unique=True)
    bank_info = models.JSONField()  # may include additional extra info

    def get(self, bank_code):
        try:
            return Bank.objects.get(bank_code=bank_code)
        except Bank.DoesNotExist:
            return None

    def add(self, data):
        Bank.objects.create(bank_name=data['bank_name'], bank_code=data['bank_code'], bank_info=data['bank_info'])

TOKEN_LIFE = 60 # seconds
class BankCheckToken(models.Model):
    card_number = models.CharField(max_length=120)
    token = models.CharField(max_length=120)
    expires = models.DateTimeField()

    def add(self, card_number, token):
        BankCheckToken.objects.create(card_number=card_number, token=token, expires=datetime.datetime.now() + datetime.timedelta(0,TOKEN_LIFE))

    def check_token(self, card_number, token):
        token = BankCheckToken.objects.get(card_number=card_number, token=token)
        if token.expires > datetime.datetime.now():
            return True
        return False

    def remove_token(self, card_number, token):
        token = BankCheckToken.objects.get(card_number=card_number, token=token)
        token.delete()