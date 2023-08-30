from django.contrib import admin

from .models import Player
# Register your models here.


class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'gender',
        'own_money',
        'credit',
        'bank',
        'shop'
    )


admin.site.register(Player, PlayerAdmin)
