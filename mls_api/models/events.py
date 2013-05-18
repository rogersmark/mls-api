from django.db import models
from mls_api.models.base import BaseModel


class Substitution(BaseModel):
    ''' Used for tracking substitutions -- currently unused '''
    out_player = models.ForeignKey('GamePlayer', related_name='subbed_out')
    in_player = models.ForeignKey('GamePlayer', related_name='subbed_in')
    team = models.ForeignKey('Team')
    minute = models.IntegerField()

    def __unicode__(self):
        return u'%s in for %s at %s' % (
            self.in_player,
            self.out_player,
            self.minute
        )

    class Meta:
        app_label = 'mls_api'


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

    class Meta:
        app_label = 'mls_api'


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

    class Meta:
        app_label = 'mls_api'
