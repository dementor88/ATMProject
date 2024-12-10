from ..atm_device.service import ATMDeviceService
from ..bank.service import BankService
from .models import ATMActivityType, ATMActivityHistory
import hashlib

class MainService(object):
    def info(self, atm_device_id):
        atm_device = ATMDeviceService().get_atm_device(atm_device_id)
        if atm_device is None:
            return 'ATM device not found'
        return atm_device.to_public_dict()

    def validate(self, card_number, pin):
        # assuming all bank system returns pin data by SHA-256 format
        pin = pin.encode('utf-8')
        sha256 = hashlib.sha256()
        sha256.update(pin)
        encrypted_pin = sha256.hexdigest()
        result = BankService().validate_pin(card_number, encrypted_pin)
        if not result['valid']:
            return 'invalid PIN'

        return result['token']

    def activity(self, activity_type, card_number, token, atm_device_id=None, balance_amount=None):
        bank_service = BankService()
        atm_service = ATMDeviceService()
        if not bank_service.check_token(card_number, token):
            return 'invalid token'

        activity_result = None
        if activity_type == ATMActivityType.SEE_BALANCE:
            activity_result = bank_service.get_account_info(card_number, token)

        if activity_result is None:
            if atm_device_id is None:
                return 'atm_device_id is required'
            if balance_amount is None:
                return 'balance_amount is required'
            elif balance_amount < 0:
                return 'balance_amount should be positive'

            if activity_type == ATMActivityType.DEPOSIT:
                activity_result = atm_service.deposit_balance(atm_device_id, balance_amount)
            elif activity_type == ATMActivityType.WITHDRAW:
                activity_result = atm_service.withdraw_balance(atm_device_id, balance_amount)
            else:
                return 'invalid activity type'

        # delete token used for identifying user account
        bank_service.remove_token(card_number, token)
        ATMActivityHistory().create(activity_type, atm_device_id, card_number)
        return activity_result