from rest_framework.test import APITestCase

from ..bank.service import BankService
from ..atm_device.service import ATMDeviceService


# Create your tests here.
class ATMTestCase(APITestCase):
    def setUp(self):
        bank_dummy = {
            'bank_name': 'Python Bank',
            'bank_code': '123456',
            'bank_info': {'Goal': 'Hello World'},
        }
        res = BankService().add_bank(bank_dummy['bank_name'], bank_dummy['bank_code'], bank_dummy['bank_info'])
        print('setup #1:', res)

        atm_dummy = {
            'atm_device_id': 'atm_1',
            'remaining_cash': 10000,
            'atm_info': {'location': 'Seoul'}
        }
        res = ATMDeviceService().create_atm_deivce(atm_dummy['atm_device_id'], atm_dummy['remaining_cash'], atm_dummy['atm_info'])
        print('setup #2:', res)

    def test_pin_validate(self):
        pass

    # def token_expired(self):
    #     pass
    #
    # def test_see_balance(self):
    #     pass
    #
    # def test_deposit(self):
    #     pass
    #
    # def test_withdraw(self):
    #     pass

