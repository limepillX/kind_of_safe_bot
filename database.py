from peewee import *

db = SqliteDatabase('database.db')


class Message(Model):
    message_id = IntegerField()
    user_id = IntegerField()

    class Meta:
        database = db
        db_table = 'messages'


db.connect()
db.create_tables([Message])
