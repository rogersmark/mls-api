from django.db import models
from mls_api.models.base import BaseModel


class Game(BaseModel):
    ''' The glue for all of the stats '''
    start_time = models.DateTimeField(blank=True, null=True)
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    competition = models.ForeignKey('Competition')
    stat_link = models.CharField(max_length=512)
    players = models.ManyToManyField('Player', through='GamePlayer')

    def __unicode__(self):
        return u'%s vs. %s on %s' % (
            self.home_team, self.away_team, self.start_time)

    @models.permalink
    def get_absolute_url(self):
        return ('game_detail', (), {'id': self.id})

    def _retrieve_goal_count(self, team):
        own_goals = self.goal_set.filter(
            own_goal=True
        ).exclude(player__team=team).count()
        goals = self.goal_set.filter(
            player__team=team,
            own_goal=False,
        ).count()
        return own_goals + goals

    @property
    def _home_score(self):
        return self._retrieve_goal_count(self.home_team)

    @property
    def _away_score(self):
        return self._retrieve_goal_count(self.away_team)

    @property
    def home_team(self):
        return self.gameteam_set.get(home=True)

    @property
    def away_team(self):
        return self.gameteam_set.get(home=False)

    @property
    def home_stats(self):
        return self.statset_set.get(team=self.home_team.team)

    @property
    def away_stats(self):
        return self.statset_set.get(team=self.away_team.team)

    class Meta:
        ordering = ('-start_time',)
        app_label = 'mls_api'
