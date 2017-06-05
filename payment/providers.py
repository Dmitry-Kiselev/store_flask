import datetime
import logging
import traceback
from abc import ABC

import stripe

from config import PaymentConfig

logger = logging.getLogger('django')


class AbstractProvider(ABC):
    charge_id = None

    def charge(self, number, exp_month, exp_year, cvc, charged_sum):
        raise NotImplementedError()


class StripeProvider(AbstractProvider):
    def __init__(self, *args, **kwargs):
        super(StripeProvider, self).__init__(*args, **kwargs)
        stripe.api_key = PaymentConfig.STRIPE_API_KEY
        self.stripe = stripe

    def charge(self, number, exp_month, exp_year, cvc, charged_sum):

        if self.charge_id:  # don't let this be charged twice!
            return Exception("Already charged.")

        try:
            response = self.stripe.Charge.create(
                amount=int(charged_sum * 100),
                currency="uah",
                card={
                    "number": number,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "cvc": cvc,
                },
                description='Thank you for your purchase!')

        except self.stripe.CardError as ce:
            logger.error('{} {}: {}'.format(datetime.datetime.now(), str(ce),
                                            traceback.format_exc()))
            # charge failed
            return ce

        self.charge_id = response.stripe_id
        return self.charge_id


class PaymentProviders(ABC):
    providers = {
        'stripe': StripeProvider,
    }

    @staticmethod
    def get_default_provider():
        return PaymentProviders.providers.get(PaymentConfig.PAYMENT_SERVICE)

    @staticmethod
    def get_provider(provider):
        return PaymentProviders.providers.get(provider)

    @staticmethod
    def add_provider(provider_name, provider_cls):
        PaymentProviders.providers[provider_name] = provider_cls
