from django.urls import path, re_path
from django.views import generic
from viewflow.flow.viewset import FlowViewSet
from django.conf.urls import url, include
from rest_framework import routers
from . import views
from . import flows
app_name = 'player_management'

router = routers.DefaultRouter()
router.register('Person', views.PersonViewSet)

a= flows.PlayerToTeamMembershipClaimFlow.urls

urlpatterns = [
    path('', views.index,  name='index'),
    path('api/', include(router.urls)),
    flows.PlayerToTeamMembershipClaimFlow.instance.urls
]