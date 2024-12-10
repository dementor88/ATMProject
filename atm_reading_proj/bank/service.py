import binascii
import os

from atm_reading_proj.bank.models import Bank, BankCheckToken


class BankService(object):
    def __init__(self):
        self.bank_cache = {}

    # in case we need to store and query bank info
    def _add_to_cache(self, bank):
        self.bank_cache[bank.bank_code] = bank

    def get_bank(self, bank_code):
        bank = self.bank_cache.get(bank_code)
        if bank is None:
            bank = Bank().get(bank_code)
            self._add_to_cache(bank)
        return bank

    def add_bank(self, data):
        Bank().add(data)

    def check_token(self, card_number, token):
        return BankCheckToken().check_token(card_number, token)

    def remove_token(self, card_number, token):
        return BankCheckToken().remove_token(card_number, token)

    def get_account_info(self, card_number, token):
        # TODO: implement real bank system
        '''
        return account info when valid else error message
        :param account:
        :return:
            {
                'bank_name': '코드은행',
                'bank_code': '12C',
                'owner': '개발자',
                'account_number': '123-456-789',
                'remaining balance': '500,000',
                'currency': 'won'
            }
        '''
        return {
            'bank_name': '코드은행',
            'bank_code': '12C',
            'owner': '개발자',
            'account_number': '123-456-789',
            'remaining balance': '500,000',
            'currency': 'won'
        }

    def validate_pin(self, card_number, encrypted_input_pin):
        # TODO: implement real bank system
        '''
        return whether encrypted_input_pin is valid or not
        :param card_number:
        :param encrypted_input_pin: encrypted data of input PIN
        :return: Access token or error message
            {
                'valid': True,
                'token': '123!@#'
                'error': '',
            }
        '''
        def generate_key():
            return binascii.hexlify(os.urandom(20)).decode()

        valid_check = True # TODO: implement actual function

        if not valid_check:
            return {'valid': False, 'error': 'PIN is not valid'}
        else:
            token = generate_key()
            BankCheckToken().add(card_number, token)
            return {'valid': valid_check, 'token': token}