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
