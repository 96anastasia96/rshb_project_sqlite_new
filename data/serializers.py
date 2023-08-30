from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Player


class PlayerSerializer(ModelSerializer):
    # equipment = serializers.StringRelatedField(many=True)
    # minigame = serializers.StringRelatedField(many=True)

    class Meta:
        model = Player
        fields = '__all__'

