from mongoengine import Document, fields, EmbeddedDocument
from datetime import datetime

class USERS(Document):
    username=fields.StringField(required=True)
    password=fields.StringField(required=True)
    firstname = fields.StringField(null=True)
    lastname = fields.StringField(null=True)
    mobilenumber = fields.StringField(null=True)

    meta={'auto_create_index': False}