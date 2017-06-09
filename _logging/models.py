from database import db


class LogRecord(db.Document):
    time = db.DateTimeField()
    url = db.StringField(max_length=180)
    method = db.StringField(max_length=5)
    host = db.StringField(max_length=100)
    user_ip = db.StringField(max_length=100)


class LogRecordError(db.Document):
    time = db.DateTimeField()
    file = db.StringField(max_length=100)
    message = db.StringField()
    traceback = db.StringField()
