# Create your views here.
import random

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@csrf_exempt
@require_POST
def payment(request):
    card_number = request.POST.get('card_number', None)
    errors_list = [
        'Ошибка сервера',
        'Банк отклонил платеж',
        'Неправильный номер счета',
        'Недостаточно средств',
        'Счет заблокирован'
    ]
    status = ''
    code = 1
    if int(card_number) % 2 or card_number[-1] == '0':
        status = random.choice(errors_list)
        code = 2
    response = {
        'status': status,
        'code': code
    }
    return JsonResponse(response)
