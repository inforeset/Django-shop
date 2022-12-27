from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView, ListView, DetailView
from app_users.forms import UserCreateForm
from django.views.generic.edit import FormMixin, UpdateView
from .forms import OrderCreateForm, OrderPaymentForm
from app_cart.cart import Cart
from app_settings.models import SiteSettings
from .models import OrderItem, Order
from .tasks import order_created
from .utils import get_delivery_price


# Create your views here.
class OrderView(FormMixin, TemplateView):
    template_name = 'app_orders/order.html'
    form_class = OrderCreateForm
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        total_cost = cart.get_total_price()
        choices = []
        settings = SiteSettings.load()
        usual_delivery_price = settings.cost_usual_delivery
        edge_delivery = settings.edge_for_free_delivery
        express_delivery_price = settings.cost_express
        context['price_usual'] = 0
        if total_cost < edge_delivery:
            choices.append(('1', f'Обычная доставка (+{usual_delivery_price} руб.)'))
            context['price_usual'] = usual_delivery_price
            context['total_with_delivery'] = total_cost + get_delivery_price(total=cart.get_total_price(),
                                                                             type_delivery='1')
        else:
            choices.append(('1', f'Обычная доставка (бесплатно)'))
        choices.append(('2', f'Экспресс доставка (+{express_delivery_price} руб.)'))
        context['form'].fields['delivery_type'].widget.choices = choices
        if self.request.user.is_authenticated:
            instance = self.request.user
            context['form_reg'] = UserCreateForm(instance=instance)
            context['form_reg'].fields['email'].disabled = True
            context['form_reg'].fields['full_name'].disabled = True
            context['form_reg'].fields['phoneNumber'].disabled = True
        else:
            context['form_reg'] = UserCreateForm()
        return context

    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.data = form.cleaned_data
            order.user = request.user
            order.delivery_price = get_delivery_price(total=cart.get_total_price(),
                                                      type_delivery=form.cleaned_data['delivery_type'])
            objs = list()
            for item in cart:
                objs.append(OrderItem(order=order,
                                      product=item['product'],
                                      price=item['price'],
                                      quantity=item['quantity']))
            order.save()
            OrderItem.objects.bulk_create(objs)
            # clear the cart
            cart.clear()
            messages.success(request, 'Заказ успешно добавлен.')
            messages.info(request, 'Ждём подтверждения оплаты от платёжной системы.')
            order_created.delay(order.id)
            return HttpResponseRedirect(reverse('order_detail', args=[order.id]))
        return super().form_invalid(form)


class HistoryOrders(LoginRequiredMixin, ListView):
    template_name = "app_orders/historyorder.html"
    raise_exception = True
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


class OrderDetail(LoginRequiredMixin, DetailView):
    template_name = "app_orders/oneorder.html"
    raise_exception = True
    model = Order
    context_object_name = 'order'

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object.user != self.request.user:
            raise PermissionDenied
        return object


class OrderPayment(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderPaymentForm
    template_name = 'app_orders/payment.html'
    raise_exception = True

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object.user != self.request.user:
            raise PermissionDenied
        return object

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        form = OrderPaymentForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            messages.info(request, 'Ждём подтверждения оплаты от платёжной системы.')
            order_created.delay(object.id)
            return HttpResponseRedirect(reverse('order_detail', args=[object.id]))
        return super().form_invalid(form)


@require_GET
@login_required
def get_order_status(request):
    order_id = request.GET.get('order_id', None)
    if not order_id:
        return JsonResponse({})
    order = Order.objects.get(id=order_id)
    if order.user != request.user:
        return JsonResponse({})
    response = {
        'status': order.status,
        'code': order.payment_code
    }
    return JsonResponse(response)
