from .service import ATMDeviceService
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def get_atm_device(request, atm_identifier):
    # TODO: implement use-case for requesting ATM device data
    return ATMDeviceService().get_atm_device(atm_identifier)

@require_http_methods(["POST"])
def create_atm_deivce(request, data):
    # TODO: implement use-case for creating bank data in DB storage
    atm_identifier = data.get("atm_identifier", None)
    if not atm_identifier:
        return 'atm_identifier is required'
    return ATMDeviceService().create_atm_deivce(atm_identifier)

@require_http_methods(["POST"])
def update_cash_amount(request, data):
    # TODO: update cash amount manually of ATM device
    atm_identifier = data.get("atm_identifier", None)
    if not atm_identifier:
        return 'atm_identifier is required'
    cash_amount = data.get("cash_amount", None)
    if not cash_amount:
        return 'cash_amount is required'
    return ATMDeviceService().update_cash_amount(atm_identifier, cash_amount)