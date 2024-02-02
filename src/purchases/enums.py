from django.db import models


class PositionTypeChose(models.IntegerChoices):
    """ Тип покупки """

    PURCHASE = 0, 'Покупка'
    SERVICE = 1, 'Услуга'
    DELIVERY = 2, 'Доставка'
