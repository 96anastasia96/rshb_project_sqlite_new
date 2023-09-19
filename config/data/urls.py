from rest_framework.routers import SimpleRouter

from .views import PlayerViewSet, EquipmentViewSet, HarvestViewSet

router = SimpleRouter()

router.register('api/v1/player', PlayerViewSet)
router.register('api/v1/equipment', EquipmentViewSet)
router.register('api/v1/harvest', HarvestViewSet)
