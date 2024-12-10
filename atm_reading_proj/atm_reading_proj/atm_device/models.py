from django.db import models

# Create your models here.
# TODO: check remaining cash of the ATM device (assuming all cash are Won)
class ATM(models.Model):
    atm_device_id = models.CharField(unique=True, max_length=100)   # may have serial number for ATM device
    remaining_cash = models.IntegerField(default=0)  # need to implement real-time cash bin checking function
    atm_info = models.JSONField()    # may include additional extra info (e.g. location, owner, A/S number) <- encrypt data if required

    def get(self, atm_device_id):
        try:
            return ATM.objects.get(atm_device_id=atm_device_id)
        except ATM.DoesNotExist:
            return None

    def create(self, atm_device_id, remaining_cash=0, atm_info=None):
        atm_device = ATM.objects.create(atm_device_id=atm_device_id, remaining_cash=remaining_cash, atm_info=atm_info)
        return atm_device.id

    def to_public_dict(self):
        return {'atm_device_id': self.atm_device_id, 'remaining_cash': self.remaining_cash, 'atm_info': self.atm_info}