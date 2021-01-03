from mongoengine import Document, StringField, ListField


class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    refresh_token = StringField()
    my_poll_ids = ListField()
    voted_poll_ids = ListField()
