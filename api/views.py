from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from app import models as app_models
from app import serializers as app_serializers



# API CRUD para ITEMS (Solo admins)
class Item(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = app_serializers.Item
    queryset = app_models.Item.objects.all()


    # Compra sin identificación
    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[],
        serializer_class=app_serializers.ItemBuy
    )
    def buy_without_identification(self, request, pk=None):
        item_obj = self.get_object()
        serializer = self.get_serializer(
            data=request.data,
            context={'item_obj': item_obj}
        )
        serializer.is_valid(raise_exception=True)
        context = serializer.save()
        return Response(context, status=status.HTTP_201_CREATED)

    
    # Compra con identificación
    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthenticated],
        serializer_class=app_serializers.ItemBuy
    )
    def buy_with_identification(self, request, pk=None):
        # Toma de datos de usuario
        user_obj = request.user
        item_obj = self.get_object()

        serializer = self.get_serializer(
            data={
                'user_id': user_obj.id,
                'quantity': request.data['quantity']
            },
            context={'item_obj': item_obj}
        )
        serializer.is_valid(raise_exception=True)
        context = serializer.save()
        return Response(context, status=status.HTTP_201_CREATED)






