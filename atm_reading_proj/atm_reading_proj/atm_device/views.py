from .service import ATMDeviceService
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def get_atm_device(request, atm_device_id):
    # TODO: implement use-case for requesting ATM device data
    return ATMDeviceService().get_atm_device(atm_device_id)

@require_http_methods(["POST"])
def create_atm_deivce(request, data):
    # TODO: implement use-case for creating bank data in DB storage
    atm_device_id = data.get("atm_device_id", None)
    if not atm_device_id:
        return 'atm_device_id is required'
    remaining_cash = data.get("remaining_cash", 0)
    atm_info = data.get("atm_info", {})
    return ATMDeviceService().create_atm_deivce(atm_device_id, remaining_cash, atm_info)

@require_http_methods(["POST"])
def update_cash_amount(request, data):
    # TODO: update cash amount manually of ATM device
    atm_device_id = data.get("atm_device_id", None)
    if not atm_device_id:
        return 'atm_device_id is required'
    cash_amount = data.get("cash_amount", None)
    if not cash_amount:
        return 'cash_amount is required'
    return ATMDeviceService().update_cash_amount(atm_device_id, cash_amount)