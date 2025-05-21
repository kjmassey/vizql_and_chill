from rest_framework.routers import DefaultRouter

from rest_framework.decorators import api_view
from tableau.views import APITest, TableauViewsSet


router = DefaultRouter()

router.register("test", APITest, basename="test")
router.register("", TableauViewsSet, basename="")

urlpatterns = [] + router.urls
