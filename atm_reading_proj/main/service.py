from atm_reading_proj.atm_device.service import ATMDeviceService
from atm_reading_proj.bank.service import BankService
from atm_reading_proj.main.models import ATMActivityType
import hashlib

class MainService(object):
    def info(self, atm_identifier):
        atm_device = ATMDeviceService().get_atm_device(atm_identifier)
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

    def activity(self, activity_type, card_number, token, atm_identifier=None, balance_amount=None):
        bank_service = BankService()
        atm_service = ATMDeviceService()
        if not bank_service.check_token(card_number, token):
            return 'invalid token'

        activity_result = None
        if activity_type == ATMActivityType.SEE_BALANCE:
            activity_result = bank_service.get_account_info(card_number, token)

        if activity_result is None:
            if atm_identifier is None:
                return 'atm_identifier is required'
            if balance_amount is None:
                return 'balance_amount is required'

            if activity_type == ATMActivityType.DEPOSIT:
                activity_result = atm_service.deposit_balance(atm_identifier, balance_amount)
            elif activity_type == ATMActivityType.WITHDRAW:
                activity_result = atm_service.withdraw_balance(atm_identifier, balance_amount)

        # delete token used for identifying user account
        bank_service.remove_token(card_number, token)
        return activity_result