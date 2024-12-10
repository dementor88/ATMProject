import datetime

from django.db import models

# Create your models here.
class ATMActivityType:
    SEE_BALANCE = 0
    DEPOSIT = 1
    WITHDRAW = 2

class ATMActivityHistory(models.Model):
    activity_date = models.DateTimeField()
    activity_type = models.IntegerField(default=ATMActivityType.SEE_BALANCE)
    # ATM info
    atm_device_id = models.CharField(max_length=100)
    # Card(Bank) info
    card_number = models.CharField(max_length=100)

    def create(self, activity_type, atm_device_id, card_number):
        ATMActivityHistory.objects.create(activity_type=activity_type, atm_device_id=atm_device_id, card_number=card_number, activity_date=datetime.datetime.now())
