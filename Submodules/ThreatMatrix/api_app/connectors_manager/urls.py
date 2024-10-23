# This file is a part of ThreatMatrix https://github.com/khulnasoft/ThreatMatrix
# See the file 'LICENSE' for copying permission.

from django.urls import include, path
from rest_framework import routers

from .views import ConnectorActionViewSet, ConnectorConfigViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter(trailing_slash=False)
router.register(
    r"jobs/(?P<job_id>\d+)/connector/(?P<report_id>\w+)",
    ConnectorActionViewSet,
    basename="connectorreport",
)
router.register(r"connector", ConnectorConfigViewSet, basename="connector")

urlpatterns = [
    path(r"", include(router.urls)),
]