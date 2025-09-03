from tortoise import fields
from tortoise.models import Model

class Item(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100)
    description = fields.TextField()
    price = fields.FloatField()
    tax = fields.FloatField(null=True)