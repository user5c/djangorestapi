from app import models as app_models
from rest_framework import serializers
from django.contrib.auth import models as auth_models


class Item(serializers.ModelSerializer):
    class Meta:
        model = app_models.Item
        fields = '__all__'


class ItemBuy(serializers.Serializer):
    user_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Purchase(serializers.ModelSerializer):
        class Item(serializers.ModelSerializer):
            class Meta:
                model = app_models.Item
                fields = '__all__'

        item = Item()

        class Meta:
            model = app_models.Purchase
            fields = '__all__'
            

    def validate(self, attrs):
        # Validar que el usuario exista (para el caso de ser llamdo de una API sin identificación)
        user_query = auth_models.User.objects.filter(id=attrs['user_id'])
        if not user_query:
            errors = {
                'user_id': ['user does not exist']
            }
            raise serializers.ValidationError(errors)

        # Validar que el Item tenga disponibilidad (para el caso de ser llamdo de una API sin identificación)
        item_obj = self.context['item_obj']
        if item_obj.quantity == 0:
            errors = {
                'item_obj': ['item not available']
            }
            raise serializers.ValidationError(errors)

        # Validar que el usuario tenga saldo
        user_obj = user_query.first()
        balance_obj = app_models.Balance.objects.get(user=user_obj)
        
        purchase_amount = item_obj.price * attrs['quantity']

        if balance_obj.value < purchase_amount:
            errors = {
                'quantity': ['user have not enough balance']
            }
            raise serializers.ValidationError(errors)
        

        return super().validate(attrs)


    def save(self, **kwargs):
        # Crear compra
        user_obj = auth_models.User.objects.get(id=self.data['user_id'])
        item_obj = self.context['item_obj']
        purchase_obj = app_models.Purchase.objects.create(
            user=user_obj,
            item=item_obj,
            quantity=self.data['quantity']
        )

        # Descontar cantidad de items comprados 
        item_obj.quantity -= self.data['quantity']
        item_obj.save()

        # Descontar saldo a usuario
        purchase_amount = item_obj.price * self.data['quantity']

        balance_obj = app_models.Balance.objects.get(user=user_obj)
        balance_obj.value -= purchase_amount
        balance_obj.save()

        purchase_rep = self.Purchase(purchase_obj)

        return purchase_rep.data


class User(serializers.ModelSerializer):
    class Meta:
        model = auth_models.User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'groups', 'date_joined')

