from rest_framework import viewsets, routers

from mls_api import models


class CompetitionViewSet(viewsets.ModelViewSet):
    model = models.Competition


class TeamViewSet(viewsets.ModelViewSet):
    model = models.Team


class GameTeamViewSet(viewsets.ModelViewSet):
    model = models.GameTeam


class StatSetViewSet(viewsets.ModelViewSet):
    model = models.StatSet


class GameViewSet(viewsets.ModelViewSet):
    model = models.Game


class PlayerViewSet(viewsets.ModelViewSet):
    model = models.Player


class GamePlayerViewSet(viewsets.ModelViewSet):
    model = models.GamePlayer


router = routers.DefaultRouter()
router.register(u'competitions', CompetitionViewSet)
router.register(u'teams', TeamViewSet)
router.register(u'games', GameViewSet)
router.register(u'players', PlayerViewSet)
router.register(u'gameplayers', GamePlayerViewSet)
router.register(u'gameteams', GameTeamViewSet)
router.register(u'gamestats', StatSetViewSet)
