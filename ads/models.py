from django.db import models


class Status(models.TextChoices):
    WAIT = 'wait', 'Ожидает'
    ACCEPTED = 'accepted', 'Принята'
    DENIED = 'denied', 'Отклонена'

class Categories(models.TextChoices):
    CARS = 'cars', 'Транспорт'
    HOUSES = 'houses', 'Недвижимость'
    PERSONAL = 'personal', 'Личные вещи'
    FOR_HOUSE = 'for_house', 'Для дома и дачи'
    SPARE_PARTS = 'spare_parts', 'Запчасти и аксессуары'
    ELECT = 'elect', 'Электроника'

class Conditions(models.TextChoices):
    NEW = 'new', "Новый"
    NOT_NEW = 'not_new', "Б/У"


class Ad(models.Model):
    user = models.IntegerField(null=False)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    image_url = models.URLField()
    category = models.CharField(max_length=30, choices=Categories)
    condition = models.CharField(max_length=15, choices=Conditions)
    created_at = models.DateTimeField(auto_now_add=True)


class ExchangeProposal(models.Model):
    ad_sender = models.IntegerField(null=False)
    ad_receiver = models.IntegerField(null=False)
    comment = models.CharField(max_length=200)
    status = models.CharField(choices=Status.choices, default=Status.WAIT, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
