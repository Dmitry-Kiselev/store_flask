from flask import render_template, request, Blueprint
from flask.views import View

from .models import LogRecord, LogRecordError

logs = Blueprint("logs", __name__)


class LogView(View):
    def dispatch_request(self):
        l = request.args.get('level')
        if l == 'error':
            logs = LogRecordError.objects.all()
        else:
            logs = LogRecord.objects.all()
        return render_template('logging/log.html', logs=logs, l=l)


logs.add_url_rule("/",
                  view_func=LogView.as_view('logs'))
