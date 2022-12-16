from django.db import models
from django.urls import reverse


class Wheat(models.Model):
    # УДАЛИТЬ: поле для первичного ключа генерируется автоматически как раз с помощью класса AutoField — переопределять его имеет смысл, только если вы явно хотите задать иной тип первичного ключа
    id = models.AutoField(primary_key=True)

    weight = models.FloatField()
    date = models.DateField(auto_now=True)

    def get_absolute_url(self):
        return reverse('wheat-create', args=[str(self.id)])

    def __str__(self):
        return f'{self.id} /{self.weight} /{self.date}'

