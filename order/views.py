from flask import render_template, flash, request, redirect, Blueprint
from flask.views import MethodView
from flask_login import current_user
from stripe import InvalidRequestError

from order.models import Order
from payment.forms import PaymentForm
from payment.models import Payment
from payment.providers import PaymentProviders

orders = Blueprint("orders", __name__)


class OrderCreateView(MethodView):
    payment_provider_class = PaymentProviders.get_default_provider()
    form_class = PaymentForm
    template_name = 'order/checkout.html'

    def get(self):
        return render_template(self.template_name, form=self.form_class())

    def post(self):
        form = self.form_class(request.form)
        if form.validate():
            basket = current_user.get_basket
            order = Order(basket=basket, discount=current_user.discount)
            basket.submit()

            basket.save()

            number = form.number.data
            exp_month = form.expiration_month.data
            exp_year = form.expiration_year.data
            cvc = form.cvc.data
            provider = self.payment_provider_class()

            try:
                charge_id = provider.charge(number, exp_month, exp_year, cvc,
                                            order.total_price)
            except InvalidRequestError:
                charge_id = None
                flash(
                    'Some error happened during checkout process. Please, try again later')

            payment = Payment(charge_id=charge_id, order=order)
            payment.save()
            flash(
                'Thanks for your order!')
            return redirect('/')


orders.add_url_rule("/checkout/",
                    view_func=OrderCreateView.as_view('checkout'))
