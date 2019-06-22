import json
import uuid

import peewee

class JSONField(peewee.TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)



class StagedEvent(peewee.Model):
    msg_uid = peewee.UUIDField(default=uuid.uuid4, index=True)
    topic = peewee.CharField(index=True)
    data = JSONField()

    sent = peewee.BooleanField(default=False, index=True)
    created_at = peewee.TimestampField(resolution=10**3)

    def to_msg(self):
        from .. import Message
        return Message(self.topic, self.msg_uid, self.data)

    @classmethod
    def unsent(cls):
        return cls.select().where(cls.sent == False)