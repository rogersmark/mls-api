from django.contrib import admin

from mls_api import models


class PlayerAdmin(admin.ModelAdmin):
    pass


class PlayerTabularInline(admin.TabularInline):
    model = models.Player


class GameAdmin(admin.ModelAdmin):
    pass


class CompetitionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        PlayerTabularInline,
    ]


class GamePlayerAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Team, TeamAdmin)
admin.site.register(models.Competition, CompetitionAdmin)
admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Game, GameAdmin)
admin.site.register(models.GamePlayer, GamePlayerAdmin)
admin.site.register(models.FormationPlayer)
admin.site.register(models.FormationLine)
admin.site.register(models.Formation)
