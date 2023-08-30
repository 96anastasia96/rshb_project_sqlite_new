from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .models import Player
from .serializers import PlayerSerializer

# Create your views here.


class PlayerViewSet(ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

