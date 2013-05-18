from django.db import models
from mls_api.models.base import BaseModel


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

    class Meta:
        app_label = 'mls_api'
