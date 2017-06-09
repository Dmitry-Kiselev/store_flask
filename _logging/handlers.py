import datetime
import logging
from logging import Handler

from .models import LogRecord, LogRecordError


class MongoLogger(Handler):
    def emit(self, record):
        if record.levelno >= logging.ERROR:
            log = LogRecordError(time=datetime.datetime.now(),
                                 file=record.pathname,
                                 message=record.msg, traceback=record.args[0])
            log.save()
        elif record.msg == 'request':
            log = LogRecord(time=datetime.datetime.now(), url=record.url,
                            method=record.method, host=record.host)
            log.save()
