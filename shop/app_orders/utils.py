import json

import requests

from app_settings.models import SiteSettings


def get_payment_status(card_number: int):
    post_data = {'card_number': card_number}
    response = requests.post("http://127.0.0.1:8000/payment/new/", data=post_data, timeout=10)
    response.raise_for_status()
    content = response.content
    result = json.loads(content.decode('utf-8'))
    return result['status'], result['code']


def get_delivery_price(total, type_delivery):
    settings = SiteSettings.load()
    usual_delivery_price = settings.cost_usual_delivery
    edge_delivery = settings.edge_for_free_delivery
    express_delivery_price = settings.cost_express
    if type_delivery == '2':
        return express_delivery_price
    if total < edge_delivery:
        return usual_delivery_price
    else:
        return 0
