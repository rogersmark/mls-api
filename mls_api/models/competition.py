from django.db import models
from mls_api.models.base import BaseModel
from .results import Result
from .team import GameTeam, Team


class Competition(BaseModel):
    ''' Competitions '''

    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    year = models.CharField(max_length=4)

    def __unicode__(self):
        return u'%s - %s' % (self.name, self.year)

    @models.permalink
    def get_absolute_url(self):
        return ('competition_detail', (), {'slug': self.slug})

    @property
    def standings(self):
        standings = Team.objects.filter(
            gameteam__game__competition=self
        ).annotate(
            models.Sum('gameteam__result__points', distinct=True)
        ).order_by(
            '-gameteam__result__points__sum'
        ).values(
            'name', 'gameteam__result__points__sum'
        )
        for team_dict in standings:
            team = Team.objects.get(name=team_dict['name'])
            games = GameTeam.objects.filter(
                team=team, game__competition=self
            )
            wins = games.filter(result__code=Result.WIN).count()
            losses = games.filter(result__code=Result.LOSS).count()
            draws = games.filter(result__code=Result.DRAW).count()
            team_dict.update({'wins': wins, 'losses': losses, 'draws': draws})

        return standings

    class Meta:
        app_label = 'mls_api'
