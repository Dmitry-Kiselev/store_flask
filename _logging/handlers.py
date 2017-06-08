import datetime
from logging import Handler

from .models import LogRecord


class MongoLogger(Handler):
    def emit(self, record):
        log = LogRecord(time=datetime.datetime.now(), file=record.pathname,
                        message=record.msg, traceback=record.exc_text,
                        level=record.levelname)
        log.save()
