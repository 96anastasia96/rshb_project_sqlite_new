from rest_framework.routers import SimpleRouter

from .views import PlayerViewSet

router = SimpleRouter()

router.register('api/v1/player', PlayerViewSet)
