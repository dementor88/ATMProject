from django.views.decorators.http import require_http_methods
from .service import MainService


# Create your views here.
@require_http_methods(["GET"])
def info(request, atm_device_id):
    return MainService().info(atm_device_id)

@require_http_methods(["POST"])
def validate(request, data):
    card_number = data.get("card_number", None)
    if card_number is None:
        return 'card_number is required'
    pin = data.get("pin", None)
    if pin is None:
        return 'pin is required'

    return MainService().validate(card_number, pin)

@require_http_methods(["POST"])
def activity(request, data):
    card_number = data.get("card_number", None)
    if card_number is None:
        return 'card_number is required'
    token = data.get("token", None)
    if token is None:
        return 'token is required'
    activity_type = data.get("activity_type", None)
    if activity_type is None:
        return 'activity_type is required'

    return MainService().activity(activity_type, card_number, token, data.get("atm_device_id"), data.get("balance_amount"))



