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
    availability = models.BooleanField(default=False)
    equipment_shop_id = models.ForeignKey(EquipmentShop, on_delete=models.CASCADE)


class Harvest(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()
    price = models.IntegerField(blank=False)
    availability = models.BooleanField(default=False)
    gen_modified = models.BooleanField(default=False)
    harvest_shop_id = models.ForeignKey(HarvestShop, on_delete=models.CASCADE, default=1)


class Minigame(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField(blank=False)
    result = models.IntegerField(default=0)


class Player(models.Model):
    genders = (
        ('Male', 'Мужчина'),
        ('Female', 'Женщина'),
        (None, 'Не указан')
    )

    name = models.CharField(max_length=20, blank=False, unique=True)
    gender = models.CharField(max_length=9, choices=genders, default=None)
    own_money = models.IntegerField(default=1000)
    credit = models.IntegerField(default=0)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, default=1)
    equipment_shop_id = models.ForeignKey(EquipmentShop, on_delete=models.CASCADE, default=1)
    harvest_shop_id = models.ForeignKey(HarvestShop, on_delete=models.CASCADE, default=1)
    equipment = models.ManyToManyField(Equipment, through='PlayerEquipment')
    harvest = models.ManyToManyField(Harvest, through='PlayerHarvest')
    minigame = models.ManyToManyField(Minigame, through='PlayerMinigame')

    def get_credit(self, credit_amount=5000):
        # bank = Bank.objects.get(id=1)
        # bank.bank_account -= credit_amount
        # bank.save()
        if self.credit == 0:
            self.credit += credit_amount
            self.own_money += credit_amount
            self.save()
            return f'Вам одобрен кредит в размере {credit_amount} руб.'
        else:
            return f'Кредит уже оформлен!'

    def return_credit(self):
        if self.credit:
            if self.own_money >= self.credit:
                # bank = Bank.objects.get(id=1)
                # bank.bank_account += self.credit
                self.own_money -= self.credit
                self.credit = 0
            else:
                raise NoCreditException('На вашем счёте недостаточно средств!')
            # bank.save()
            self.save()
            return f'Кредит возращён.'
        else:
            raise NotEnoughFundsException('У вас нет кредита!')

    def tomato_amount(self):
        return PlayerHarvest.objects.get(player_id=self.id, harvest_id=1).harvest_amount

    def pepper_amount(self):
        return PlayerHarvest.objects.get(player_id=self.id, harvest_id=2).harvest_amount

    def strawberry_amount(self):
        return PlayerHarvest.objects.get(player_id=self.id, harvest_id=3).harvest_amount


class PlayerEquipment(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    equipment_id = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    def __str__(self):
        return (f'player_id: {self.player_id.id}, '
                f'equipment_id: {self.equipment_id.id}')


class PlayerHarvest(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    harvest_id = models.ForeignKey(Harvest, on_delete=models.CASCADE)
    harvest_amount = models.IntegerField(default=0)

    def __str__(self):
        return (f'player_id: {self.player_id.id}, '
                f'harvest_id: {self.harvest_id.id}, '
                f'harvest_amount: {self.harvest_amount}')


class PlayerMinigame(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    minigame_id = models.ForeignKey(Minigame, on_delete=models.CASCADE)

