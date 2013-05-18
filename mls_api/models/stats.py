from django.db import models
from mls_api.models.base import BaseModel


class StatSet(BaseModel):
    ''' Holds all the basic stats of a game such as possession, shots on goal
    so on and so forth
    '''

    attempts_on_goal = models.IntegerField()
    shots_on_target = models.IntegerField()
    shots_off_target = models.IntegerField()
    blocked_shots = models.IntegerField()
    corner_kicks = models.IntegerField()
    fouls = models.IntegerField()
    crosses = models.IntegerField()
    offsides = models.IntegerField()
    first_yellows = models.IntegerField()
    second_yellows = models.IntegerField()
    red_cards = models.IntegerField()
    duels_won = models.IntegerField()
    duels_won_percentage = models.IntegerField()
    total_passes = models.IntegerField()
    pass_percentage = models.IntegerField()
    possession = models.DecimalField(decimal_places=2, max_digits=4)
    team = models.ForeignKey('Team')
    game = models.ForeignKey('Game')

    def __unicode__(self):
        return u'Stats for %s' % self.game

    class Meta:
        app_label = 'mls_api'
