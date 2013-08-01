from django.db import models
from mls_api.models.base import BaseModel


class Team(BaseModel):
    ''' Soccer teams '''

    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    games = models.ManyToManyField('Game', through='GameTeam')

    def __unicode__(self):
        return u'%s' % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('team_detail', (), {'slug': self.slug})

    def points_by_comp(self, competition):
        return self.gameteam_set.filter(
            game__competition__year=2013
        ).aggregate(models.Sum('result__points'))['result__points__sum']

    class Meta:
        ordering = ('name',)
        app_label = 'mls_api'


class GameTeam(BaseModel):

    team = models.ForeignKey('Team')
    game = models.ForeignKey('Game')
    result = models.ForeignKey('Result')
    home = models.BooleanField(default=False)

    def __unicode__(self):
        return self.team.__unicode__()

    class Meta:
        app_label = 'mls_api'
