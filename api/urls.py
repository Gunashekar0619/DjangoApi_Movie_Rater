from .views import MViewSet, RViewSet, UViewSet
from django.urls import path
from rest_framework import routers
from django.conf.urls import include

router = routers.DefaultRouter()
router.register('user', UViewSet)
router.register('movie', MViewSet)
router.register('rating', RViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
