from database import db


class LogRecord(db.Document):
    time = db.DateTimeField()
    file = db.StringField(max_length=100)
    message = db.StringField()
    traceback = db.StringField()
    level = db.StringField(max_length=30)
