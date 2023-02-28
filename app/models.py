from django.db import models


class Balance(models.Model):
    user = models.ForeignKey('auth.User', models.CASCADE)
    value = models.BigIntegerField(default=0)


class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.id}, {self.name} ({self.quantity})"


class Purchase(models.Model):
    user = models.ForeignKey('auth.User', models.CASCADE)
    item = models.ForeignKey(Item, models.CASCADE)
    quantity = models.IntegerField(default=1)
