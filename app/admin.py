from django.contrib import admin
from . import models



@admin.register(models.Balance)
class Balance(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'value'
    ]


@admin.register(models.Item)
class Item(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'price',
        'quantity'
    ]


@admin.register(models.Purchase)
class Purchase(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'item',
        'quantity'
    ]