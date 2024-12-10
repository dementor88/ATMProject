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
    atm_identifier = models.CharField(max_length=120)
    atm_withdraw_result = models.JSONField()
    # Card(Bank) info
    card_number = models.CharField(max_length=120)
    card_identification_result = models.JSONField()
