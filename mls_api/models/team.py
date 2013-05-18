from django.db import models
from mls_api.models.base import BaseModel


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
        app_label = 'mls_api'
