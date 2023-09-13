from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Player, Equipment, Harvest


class PlayerSerializer(ModelSerializer):
    # equipment = serializers.StringRelatedField(many=True)
    # minigame = serializers.StringRelatedField(many=True)

    class Meta:
        model = Player
        fields = '__all__'


class EquipmentShopSerializer(ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'


class HarvestShopSerializer(ModelSerializer):
    class Meta:
        model = Harvest
        fields = '__all__'