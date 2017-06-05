from wtforms import Form, StringField, IntegerField
from wtforms.widgets import TextInput


class PaymentForm(Form):
    number = StringField(label="Card Number")
    expiration_month = StringField(label="Expiration month")
    expiration_year = StringField(label="Expiration year")
    cvc = IntegerField(label="CCV Number",
                       widget=TextInput())

    provider = None

    def validate(self):
        if not super(PaymentForm, self).validate():
            return False
        if not self.validate_card(self.number.data):
            return False
        return True

    def validate_card(self, number):
        digits = [int(i) for i in str(number)]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        total = sum(odd_digits)
        for digit in even_digits:
            total += sum([int(i) for i in str(2 * digit)])
        return total % 10 == 0
