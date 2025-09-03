from tortoise import fields
from tortoise.models import Model

class Item(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    description = fields.TextField()
    price = fields.FloatField()
    tax = fields.FloatField(null=True)