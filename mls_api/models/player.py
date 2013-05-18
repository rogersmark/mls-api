from django.db import models
from mls_api.models.base import BaseModel, POSITIONS


class Player(BaseModel):
    ''' Soccer players '''

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    number = models.IntegerField()
    team = models.ForeignKey('Team')
    position = models.CharField(
        max_length=32,
        choices=POSITIONS
    )

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    @models.permalink
    def get_absolute_url(self):
        return ('player_detail', (), {'id': self.id})

    class Meta:
        ordering = ('last_name', 'first_name')
        app_label = 'mls_api'


class PlayerStatLine(BaseModel):
    ''' Used for collecting the stat line for a player in a game '''

    player = models.ForeignKey('GamePlayer')
    shots = models.IntegerField(default=0)
    shots_on_goal = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    fouls_commited = models.IntegerField(default=0)
    fouls_suffered = models.IntegerField(default=0)
    corners = models.IntegerField(default=0)
    offsides = models.IntegerField(default=0)
    saves = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)

    def __unicode__(self):
        return u'Stats for %s' % self.player

    class Meta:
        app_label = 'mls_api'


class GamePlayer(BaseModel):
    ''' Used for mapping players to specific games '''

    player = models.ForeignKey(Player)
    position = models.CharField(max_length=32,
        choices=POSITIONS)
    game = models.ForeignKey('Game')
    captain = models.BooleanField(default=False)
    team = models.ForeignKey('Team')

    def __unicode__(self):
        return u'%s %s' % (self.player.first_name, self.player.last_name)

    class Meta:
        app_label = 'mls_api'
