from application import db
from user.models import User

class Study(db.Document):
    name = db.StringField(required=True)
    place = db.StringField(required=True)
    theme = db.StringField(required=True)
    tag = db.ListField(required=True)
    start_datetime = db.DateTimeField(required=True)
    end_datetime = db.DateTimeField(required=True)
    study_photo = db.StringField()
    description = db.StringField(min_length=50, required=True)
    host = db.ObjectIdField(required=True)
    cancel = db.BooleanField(default=False)
    attendees = db.ListField(db.ReferenceField(User))

class Theme(db.Document):
    name = db.StringField(required=True)
    subscribers = db.ListField(db.ReferenceField(User))
    description = db.StringField(min_length=50, required=True)
    cancel = db.BooleanField(default=False)

# class Tag(db.Document):
#     name = db.StringField(required=True)
