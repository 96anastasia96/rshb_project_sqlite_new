import json

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK

from.models import Bank, Shop, Player
from.serializers import PlayerSerializer


class PlayerApiTestCase(APITestCase):
    def setUp(self):
        self.bank = Bank.objects.create()
        self.shop = Shop.objects.create()
        self.player = Player.objects.create(
            name='test',
            gender='Женщина',
            bank=self.bank,
            shop=self.shop
        )
        self.url = reverse('player-list')

    def test_get(self):

        response = self.client.get(self.url)
        serializer_data = PlayerSerializer(self.player).data
        response_data = json.loads(json.dumps(response.data))
        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, *response_data)
