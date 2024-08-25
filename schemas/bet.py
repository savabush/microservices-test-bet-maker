from tortoise import Model, fields

from models.bet import BetState


class BetModel(Model):
    id = fields.IntField(pk=True, description="ID")
    event_id = fields.IntField(description="ID события")
    sum = fields.DecimalField(max_digits=8, decimal_places=2, description="Сумма")
    status = fields.CharEnumField(BetState, description="Статус", default=BetState.NOT_FINISHED)
