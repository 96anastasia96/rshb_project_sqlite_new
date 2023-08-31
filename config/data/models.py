from django.contrib.auth.models import User

from django.db import models

from .exceptions import NoCreditException, NotEnoughFundsException

# Create your models here.


class Bank(models.Model):
    bank_account = models.IntegerField(default=1000000)


class Shop(models.Model):
    bank_account = models.IntegerField(default=0)


class Equipment(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()
    price = models.IntegerField(blank=False)
    availability = models.BooleanField(default=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)


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
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, default=1)
    equipment = models.ManyToManyField(Equipment, through='PlayerEquipment')
    minigame = models.ManyToManyField(Minigame, through='PlayerMinigame')

    def get_credit(self, credit_amount=5000):
        bank = Bank.objects.get(id=1)
        bank.bank_account -= credit_amount
        bank.save()
        self.credit += credit_amount
        self.own_money += credit_amount
        self.save()


    def return_credit(self):
        if self.credit:
            if self.own_money >= self.credit:
                bank = Bank.objects.get(id=1)
                bank.bank_account += self.credit
                self.own_money -= self.credit
                self.credit = 0
            else:
                raise NoCreditException('На вашем счёте недостаточно средств!')
            bank.save()
            self.save()
        else:
            raise NotEnoughFundsException('У вас нет кредита!')


class PlayerEquipment(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)


class PlayerMinigame(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    minigame = models.ForeignKey(Minigame, on_delete=models.CASCADE)

