from .service import BankService
from django.views.decorators.http import require_http_methods

# Create your views here.
@require_http_methods(["GET"])
def get_bank(request, bank_code):
    # TODO: implement use-case for requesting stored bank data
    return BankService().get_bank(bank_code)

@require_http_methods(["POST"])
def add_bank(request, data):
    # TODO: implement use-case for creating bank data in DB storage
    bank_code = data.get("bank_code", None)
    if not bank_code:
        return 'bank_code is required'
    bank_name = data.get("bank_name", None)
    if not bank_name:
        return 'bank_name is required'
    bank_info = data.get("bank_info", None)
    return BankService().add_bank(bank_code, bank_name, bank_info)