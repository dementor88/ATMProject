from .models import ATM


class ATMDeviceService(object):
    def __init__(self):
        self.atm_cache = {}

    def _add_to_cache(self, atm):
        self.atm_cache[atm.atm_device_id] = atm

    def get_atm_device(self, atm_device_id):
        atm_device = self.atm_cache.get(atm_device_id)
        if atm_device is None:
            atm_device = ATM().get(atm_device_id)
            if atm_device is not None:
                self._add_to_cache(atm_device)
        return atm_device

    def create_atm_deivce(self, atm_device_id, remaining_cash, atm_info):
        return ATM().create(atm_device_id, remaining_cash, atm_info)

    def deposit_balance(self, atm_device_id, balance_amount):
        # TODO: update cash amount of ATM device after deposit
        '''
        update cash amount of ATM device after deposit
        :param atm_device_id: identifier of ATM device
        :param balance_amount: amount of deposit
        :return: True if process is successful, else False
        '''
        atm_device = self.get_atm_device(atm_device_id)
        if atm_device is None:
            return 'atm_device_id is invalid'
        atm_device.remaining_cash=atm_device.remaining_cash + balance_amount
        atm_device.save()
        return True     # TODO: need to return remaining balance in account

    def withdraw_balance(self, atm_device_id, balance_amount):
        # TODO: check withdraw is possible, and update cash amount of ATM device after withdraw
        '''
        check withdraw is possible, and update cash amount of ATM device after withdraw
        :param atm_device_id: identifier of ATM device
        :param balance_amount: amount of deposit
        :return: True if withdraw and cash update is successful, else False
        '''
        atm_device = self.get_atm_device(atm_device_id)
        if atm_device is None:
            return 'atm_device_id is invalid'
        if atm_device.remaining_cash > balance_amount:
            atm_device.remaining_cash=atm_device.remaining_cash - balance_amount
            atm_device.save()
            return True     # TODO: need to return remaining balance in account
        return 'atm_device does not have enough cash'

    def update_cash_amount(self, atm_device_id, cash_amount):
        # TODO: update cash amount of ATM device
        '''
        update cash amount of ATM device
        :param atm_device_id: identifier of ATM device
        :param cash_amount: new amount of cash
        :return: True if cash update is successful, else False
        '''
        atm_device = self.get_atm_device(atm_device_id)
        if atm_device is None:
            return False
        atm_device.remaining_cash=cash_amount
        atm_device.save()
        return True

