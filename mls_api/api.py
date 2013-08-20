from rest_framework import viewsets, routers, serializers, fields

from mls_api import models


class CompetitionSerializer(serializers.ModelSerializer):

    standings = fields.Field(source='standings')

    class Meta:
        model = models.Competition


class CompetitionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Competition.objects.all()
    serializer_class = CompetitionSerializer


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.Team
    filter_fields = ('name', 'slug',)


class GameTeamViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.GameTeam


class StatSetViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.StatSet


class GameSerializer(serializers.HyperlinkedModelSerializer):

    statset_set = serializers.HyperlinkedRelatedField(
        view_name='statset-detail',
        lookup_field='pk',
        many=True,
        read_only=True,
    )

    class Meta:
        model = models.Game


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Game.objects.all()
    serializer_class = GameSerializer


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.Player
    filter_fields = ('first_name', 'last_name', 'team__name')


class GamePlayerViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.GamePlayer


router = routers.DefaultRouter()
router.register(u'competitions', CompetitionViewSet)
router.register(u'teams', TeamViewSet)
router.register(u'games', GameViewSet)
router.register(u'players', PlayerViewSet)
router.register(u'gameplayers', GamePlayerViewSet)
router.register(u'gameteams', GameTeamViewSet)
router.register(u'gamestats', StatSetViewSet)
