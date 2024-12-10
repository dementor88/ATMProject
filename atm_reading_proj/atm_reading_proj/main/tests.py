from rest_framework.test import APITestCase

from .service import MainService
from .models import ATMActivityType
from ..bank.service import BankService
from ..atm_device.service import ATMDeviceService
import time
from django.conf import settings

TOKEN_LIFE = settings.TOKEN_LIFE

# Create your tests here.
class ATMTestCase(APITestCase):
    def setUp(self):
        self.bank_service = BankService()
        self.atm_service = ATMDeviceService()
        self.main_service = MainService()

        self.atm_dummy = {
            'atm_device_id': 'atm_1',
            'remaining_cash': 10000,
            'atm_info': {'location': 'Seoul'}
        }
        res = self.atm_service.create_atm_deivce(self.atm_dummy['atm_device_id'], self.atm_dummy['remaining_cash'], self.atm_dummy['atm_info'])

    def test_atm_device_data(self):
        print('check_atm_device_data...')
        right_device_id = 'atm_1'
        info = self.main_service.info(right_device_id)
        self.assertEqual(info['remaining_cash'], self.atm_dummy['remaining_cash'])
        self.assertEqual(info['atm_info'], self.atm_dummy['atm_info'])

        wrong_device_id = 'atm_2'
        info = self.main_service.info(wrong_device_id)
        self.assertEqual(info, 'ATM device not found')

    def test_pin_validate(self):
        print('test_pin_validate...')
        card_number = '123-456-789-456'
        pin = '1234'
        token = self.main_service.validate(card_number, pin)
        self.assertTrue('invalid PIN' not in token)

        with self.settings(BANK_SYSTEM_TESTRUN=False):
            token = self.main_service.validate(card_number, pin)
            self.assertTrue('invalid PIN' == token)

    def test_token_expired(self):
        print('test_token_expired...')
        card_number = '123-456-789-456'
        pin = '1234'
        token = self.main_service.validate(card_number, pin)
        self.assertTrue('invalid PIN' not in token)

        token_alive = self.bank_service.check_token(card_number, token)
        self.assertEqual(token_alive, True)

        time.sleep(TOKEN_LIFE)
        token_alive = self.bank_service.check_token(card_number, token)
        self.assertEqual(token_alive, False)

    def test_see_balance(self):
        print('test_see_balance...')
        card_number = '123-456-789-456'
        pin = '1234'
        atm_device_id = self.atm_dummy['atm_device_id']
        token = self.main_service.validate(card_number, pin)
        self.assertTrue('invalid PIN' not in token)

        account_info = self.main_service.activity(ATMActivityType.SEE_BALANCE, card_number, token, atm_device_id)
        self.assertEqual(set(account_info.keys()), {'bank_name', 'bank_code', 'owner', 'account_number', 'remaining_balance'})
        self.assertEqual(account_info['remaining_balance'], 500000)


    def test_deposit(self):
        print('test_see_balance...')
        card_number = '123-456-789-456'
        pin = '1234'
        atm_device_id = self.atm_dummy['atm_device_id']
        balance_amount = 5000
        token = self.main_service.validate(card_number, pin)
        self.assertTrue('invalid PIN' not in token)

        deposit_result = self.main_service.activity(ATMActivityType.DEPOSIT, card_number, token, atm_device_id, balance_amount)
        self.assertEqual(deposit_result, True)

        atm_info = self.atm_service.get_atm_device(atm_device_id)
        self.assertEqual(atm_info.remaining_cash, balance_amount + self.atm_dummy['remaining_cash'])

    def test_withdraw(self):
        print('test_see_balance...')
        card_number = '123-456-789-456'
        pin = '1234'
        atm_device_id = self.atm_dummy['atm_device_id']
        balance_amount = 7000
        token = self.main_service.validate(card_number, pin)
        self.assertTrue('invalid PIN' not in token)

        deposit_result = self.main_service.activity(ATMActivityType.WITHDRAW, card_number, token, atm_device_id, balance_amount)
        self.assertEqual(deposit_result, True)

        atm_info = self.atm_service.get_atm_device(atm_device_id)
        self.assertEqual(atm_info.remaining_cash, self.atm_dummy['remaining_cash'] - balance_amount)

        # test withdrawing more than cash in ATM
        token = self.main_service.validate(card_number, pin)
        self.assertTrue('invalid PIN' not in token)

        deposit_result = self.main_service.activity(ATMActivityType.WITHDRAW, card_number, token, atm_device_id, balance_amount)
        self.assertTrue(deposit_result == 'atm_device does not have enough cash')

        atm_info = self.atm_service.get_atm_device(atm_device_id)
        self.assertTrue(atm_info.remaining_cash > 0)


    def test_wrong_activity_type(self):
        print('test_wrong_activity_type...')
        card_number = '123-456-789-456'
        pin = '1234'
        atm_device_id = self.atm_dummy['atm_device_id']
        token = self.main_service.validate(card_number, pin)
        self.assertTrue('invalid PIN' not in token)

        response = self.main_service.activity('wrong type', card_number, token, atm_device_id)
        self.assertTrue('invalid activity type' == response)

    def test_wrong_atm_device_id_for_deposit(self):
        print('test_wrong_atm_device_id_in_deposit...')
        card_number = '123-456-789-456'
        pin = '1234'
        atm_device_id = self.atm_dummy['atm_device_id']
        wrong_atm_device_id = 'atm_2'
        balance_amount = 5000
        token = self.main_service.validate(card_number, pin)
        self.assertTrue('invalid PIN' not in token)

        deposit_result = self.main_service.activity(ATMActivityType.DEPOSIT, card_number, token, wrong_atm_device_id, balance_amount)
        self.assertTrue(deposit_result == 'atm_device_id is invalid')


    def test_wrong_card_and_token_pair(self):
        print('test_wrong_card_and_token_pair...')
        card_number = '123-456-789-456'
        wrong_card_number = '789-456-789-456'
        pin = '1234'
        atm_device_id = self.atm_dummy['atm_device_id']
        token = self.main_service.validate(card_number, pin)
        self.assertTrue('invalid PIN' not in token)

        response = self.main_service.activity(ATMActivityType.SEE_BALANCE, wrong_card_number, token, atm_device_id)
        self.assertTrue('invalid token' == response)