from django.contrib.auth.models import User

from django.db import models

from .exceptions import NoCreditException, NotEnoughFundsException

# Create your models here.


class Bank(models.Model):
    bank_account = models.IntegerField(default=1000000)


class EquipmentShop(models.Model):
    name = models.CharField(max_length=50, default='Своё Фермерство', blank=False)


class HarvestShop(models.Model):
    name = models.CharField(max_length=50, default='Своё Родное', blank=False)


class Equipment(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()
    price = models.IntegerField(blank=False)
    equipment_shop_id = models.ForeignKey(EquipmentShop, on_delete=models.CASCADE)


class Harvest(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()
    price = models.IntegerField(blank=False)
    harvest_shop_id = models.ForeignKey(HarvestShop, on_delete=models.CASCADE, default=1)


class Minigame(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField(blank=False)


class Player(models.Model):
    genders = (
        ('Male', 'Мужчина'),
        ('Female', 'Женщина'),
        (None, 'Не указан')
    )

    name = models.CharField(max_length=20, blank=False, unique=True)
    gender = models.CharField(max_length=9, choices=genders, default=None)
    own_money = models.IntegerField(default=1000)
    own_coins = models.IntegerField(default=100)
    credit = models.IntegerField(default=0)
    bank_id = models.ForeignKey(Bank, on_delete=models.CASCADE, default=1)
    equipment_shop_id = models.ForeignKey(EquipmentShop, on_delete=models.CASCADE, default=1)
    harvest_shop_id = models.ForeignKey(HarvestShop, on_delete=models.CASCADE, default=1)
    equipment = models.ManyToManyField(Equipment, through='PlayerEquipment')
    harvest = models.ManyToManyField(Harvest, through='PlayerHarvest')
    minigame = models.ManyToManyField(Minigame, through='PlayerMinigame')

    def get_credit(self, credit_amount=1000):
        if self.credit == 0:
            self.credit += credit_amount
            self.own_money += credit_amount
            self.save()
            return (f'Вам одобрен кредит в размере {credit_amount} руб.'
                    f'На Вашем счёте {self.own_money} руб.')
        else:
            return f'Кредит уже оформлен!'

    def return_credit(self):
        if self.credit:
            if self.own_money >= self.credit+30:
                self.own_money -= self.credit+30
                self.credit = 0
            else:
                raise NoCreditException('На Вашем счёте недостаточно средств!')
            self.save()
            return (f'Кредит возращён. '
                    f'На Вашем счёте {self.own_money} руб.')
        else:
            raise NotEnoughFundsException('У вас нет кредита!')

#  Метод для обновления результатов у пользователя по ID
    def update_minigame_result(self, minigame_id, result):
        player_minigame = PlayerMinigame.objects.filter(player=self, minigame__id=minigame_id).first()
        if player_minigame:
            player_minigame.result = result
            player_minigame.save()
        else:
            raise ValueError(f"Запись об игроке ={self.id} и мини-игра ={minigame_id} не найдены")


class PlayerEquipment(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    equipment_id = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    availability = models.BooleanField(default=False)

    def __str__(self):
        return (f'player_id: {self.player_id.id}, '
                f'equipment_id: {self.equipment_id.id}')

    def change_availability(self):
        self.availability = True
        self.save()


class PlayerHarvest(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    harvest_id = models.ForeignKey(Harvest, on_delete=models.CASCADE)
    harvest_amount = models.IntegerField(default=0)
    availability = models.BooleanField(default=False)
    gen_modified = models.BooleanField(default=False)

    def __str__(self):
        return (f'player_id: {self.player_id.id}, '
                f'harvest_id: {self.harvest_id.id}, '
                f'harvest_amount: {self.harvest_amount}')

    def change_gen_modified(self):
        self.gen_modified = True
        self.save()
        return f'Процес генной модификации прошёл успешно!'

    def change_availability(self):
        self.availability = True
        self.save()


class PlayerMinigame(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    minigame_id = models.ForeignKey(Minigame, on_delete=models.CASCADE)
    result = models.IntegerField(default=0)

    def change_result(self, res):
        player = Player.objects.get(id=self.player_id)
        players_harvest = PlayerHarvest.objects.filter(player_id=self.player_id)

        players_harvest_mod = list(map(lambda x: x.change_gen_modified, players_harvest))
        [i.save() for i in players_harvest_mod]

        player.own_coins += res
        player.save()


