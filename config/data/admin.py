from django.contrib import admin

from .models import Player, Equipment, Harvest, PlayerHarvest, PlayerEquipment
# Register your models here.


class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'gender',
        'own_money',
        'credit',
        'bank_id',
        'equipment_shop_id',
        'harvest_shop_id',
    )


class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'price',
        'equipment_shop_id'
    )


class HarvestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'price',
        'harvest_shop_id',
    )


admin.site.register(Player, PlayerAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Harvest, HarvestAdmin)
admin.site.register(PlayerHarvest)
admin.site.register(PlayerEquipment)