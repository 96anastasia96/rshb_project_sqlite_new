from rest_framework.routers import SimpleRouter

from .views import PlayerViewSet, EquipmentShopViewSet, HarvestShopViewSet

router = SimpleRouter()

router.register('api/v1/player', PlayerViewSet)
router.register('api/v1/equipment_shop', EquipmentShopViewSet)
router.register('api/v1/harvest_shop', HarvestShopViewSet)
