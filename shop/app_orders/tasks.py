from django.db import transaction, IntegrityError
from requests import HTTPError, ConnectTimeout, ReadTimeout, Timeout

from .models import Order
from app_shop.models import Product

from shop.celery_task import app

from .utils import get_payment_status


@app.task()
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    status = ''
    payment_code = order.payment_code
    objs_store = list()
    try:
        for good in order.items.all():
            store_good = Product.objects.select_for_update().get(id=good.product.id)
            if good.quantity > store_good.stock:
                status = f'{good.product.name} недостаточно на складе'
                raise IntegrityError
            store_good.stock -= good.quantity
            objs_store.append(store_good)
        with transaction.atomic():
            if not status:
                Product.objects.bulk_update(objs_store, ['stock'])
                status, payment_code = get_payment_status(order.card_number)
                if payment_code == 1:
                    order.paid = True
    except IntegrityError:
        payment_code = 2
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
        payment_code = 3
        status = "Нет связи с сервером оплаты"

    order.status = status
    order.payment_code = payment_code
    order.save()
