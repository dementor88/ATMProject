from django.db import models
import JSONField

# Create your models here.
# TODO: check remaining cash of the ATM device
class ATM(models.Model):
    atm_identifier = models.CharField(unique=True)
    remaining_cash = models.IntegerField()  # need to implement real-time cash bin checking function
    atm_info = models.JSONField()    # may include additional extra info (e.g. location, owner, A/S number) <- encrypt data if required

    def get(self, atm_identifier):
        try:
            return ATM.objects.get(atm_identifier=atm_identifier)
        except ATM.DoesNotExist:
            return None

    def create(self, data):
        ATM.objects.create(remaining_cash=data['remaining_cash'], atm_info=data['atm_info'])

    def to_public_dict(self):
        return {'atm_identifier': self.atm_identifier, 'remaining_cash': self.remaining_cash, 'atm_info': self.atm_info}