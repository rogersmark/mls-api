from django.db import models
from mls_api.models.base import BaseModel


class FormationPlayer(BaseModel):
    ''' This is another M2M Through Model. We need this to track what
    position a player was in within a Formation Line
    '''

    player = models.ForeignKey('GamePlayer')
    line = models.ForeignKey('FormationLine')
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ('sort_order',)
        app_label = 'mls_api'


class FormationLine(BaseModel):
    ''' One line in a formation '''

    players = models.ManyToManyField('GamePlayer', through='FormationPlayer')
    formation = models.ForeignKey('Formation')
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ('sort_order',)
        app_label = 'mls_api'


class Formation(BaseModel):
    ''' Model for tracking formations '''

    team = models.ForeignKey('Team')
    game = models.ForeignKey('Game')

    @property
    def formation_str(self):
        return '-'.join(
            [str(x.players.count()) for x in self.formationline_set.all()][1:]
        )

    def __unicode__(self):
        return u'%s: %s %s' % (
            self.team,
            self.formation_str,
            self.game.start_time
        )

    class Meta:
        app_label = 'mls_api'
