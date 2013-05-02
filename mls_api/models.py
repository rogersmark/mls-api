from django.db import models

POSITIONS = (
    ('G', 'Goalkeeper'),
    ('D', 'Defender'),
    ('M', 'Midfielder'),
    ('F', 'Forward'),
    ('S', 'Sub'),
)


class BaseModel(models.Model):
    ''' Simple abstract base model '''

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Team(BaseModel):
    ''' Soccer teams '''

    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return u'%s' % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('team_detail', (), {'slug': self.slug})

    class Meta:
        ordering = ('name',)


class Player(BaseModel):
    ''' Soccer players '''

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    number = models.IntegerField()
    team = models.ForeignKey(Team)
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


class Game(BaseModel):
    ''' The glue for all of the stats '''
    home_team = models.ForeignKey(Team, related_name="home_team")
    away_team = models.ForeignKey(Team, related_name="away_team")
    start_time = models.DateTimeField(blank=True, null=True)
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    competition = models.ForeignKey(Competition)
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
    def home_score(self):
        return self._retrieve_goal_count(self.home_team)

    @property
    def away_score(self):
        return self._retrieve_goal_count(self.away_team)

    class Meta:
        ordering = ('-start_time',)


class Substitution(BaseModel):
    ''' Used for tracking substitutions -- currently unused '''
    out_player = models.ForeignKey('GamePlayer', related_name='subbed_out')
    in_player = models.ForeignKey('GamePlayer', related_name='subbed_in')
    team = models.ForeignKey(Team)
    minute = models.IntegerField()

    def __unicode__(self):
        return u'%s in for %s at %s' % (
            self.in_player,
            self.out_player,
            self.minute
        )


class Goal(BaseModel):
    ''' Records goal events '''

    game = models.ForeignKey('Game')
    minute = models.IntegerField()
    player = models.ForeignKey('GamePlayer')
    penalty = models.BooleanField(default=False)
    own_goal = models.BooleanField(default=False)
    assisted_by = models.ManyToManyField(
        'GamePlayer',
        related_name='assists'
    )

    def __unicode__(self):
        return u"Goal by %s at %s'" % (self.player, self.minute)


class Booking(BaseModel):
    ''' Used for tracking disciplinary actions -- Currently unused '''

    CARD_COLOR = (
        ('yellow', 'Yellow'),
        ('red', 'Red')
    )

    game = models.ForeignKey('Game')
    minute = models.IntegerField()
    player = models.ForeignKey('GamePlayer')
    card_color = models.CharField(max_length=8, choices=CARD_COLOR)
    reason = models.CharField(max_length=256)

    def __unicode__(self):
        return u"%s card for %s at %s'" % (
            self.get_card_color_display(),
            self.player,
            self.minute
        )
