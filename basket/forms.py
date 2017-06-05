from wtforms import Form, IntegerField

class LineForm(Form):
    quantity = IntegerField(label='quantity', default=1)
    line_id = IntegerField()
