# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PlayerStatLine'
        db.create_table(u'mls_api_playerstatline', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mls_api.GamePlayer'])),
            ('shots', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('shots_on_goal', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('minutes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('goals', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('assists', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fouls_commited', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fouls_suffered', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('corners', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('offsides', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('saves', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('goals_against', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'mls_api', ['PlayerStatLine'])


    def backwards(self, orm):
        # Deleting model 'PlayerStatLine'
        db.delete_table(u'mls_api_playerstatline')


    models = {
        u'mls_api.booking': {
            'Meta': {'object_name': 'Booking'},
            'card_color': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minute': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.GamePlayer']"}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'mls_api.competition': {
            'Meta': {'object_name': 'Competition'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        u'mls_api.formation': {
            'Meta': {'object_name': 'Formation'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Team']"})
        },
        u'mls_api.formationline': {
            'Meta': {'ordering': "('sort_order',)", 'object_name': 'FormationLine'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'formation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Formation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['mls_api.GamePlayer']", 'through': u"orm['mls_api.FormationPlayer']", 'symmetrical': 'False'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'mls_api.formationplayer': {
            'Meta': {'ordering': "('sort_order',)", 'object_name': 'FormationPlayer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.FormationLine']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.GamePlayer']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'mls_api.game': {
            'Meta': {'ordering': "('-start_time',)", 'object_name': 'Game'},
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_team'", 'to': u"orm['mls_api.Team']"}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Competition']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_team'", 'to': u"orm['mls_api.Team']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['mls_api.Player']", 'through': u"orm['mls_api.GamePlayer']", 'symmetrical': 'False'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'stat_link': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'mls_api.gameplayer': {
            'Meta': {'object_name': 'GamePlayer'},
            'captain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Player']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Team']"})
        },
        u'mls_api.goal': {
            'Meta': {'object_name': 'Goal'},
            'assisted_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assists'", 'symmetrical': 'False', 'to': u"orm['mls_api.GamePlayer']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minute': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'own_goal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'penalty': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.GamePlayer']"})
        },
        u'mls_api.player': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'Player'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Team']"})
        },
        u'mls_api.playerstatline': {
            'Meta': {'object_name': 'PlayerStatLine'},
            'assists': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'corners': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fouls_commited': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fouls_suffered': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'goals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'goals_against': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minutes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'offsides': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.GamePlayer']"}),
            'saves': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shots': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shots_on_goal': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'mls_api.statset': {
            'Meta': {'object_name': 'StatSet'},
            'attempts_on_goal': ('django.db.models.fields.IntegerField', [], {}),
            'blocked_shots': ('django.db.models.fields.IntegerField', [], {}),
            'corner_kicks': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'crosses': ('django.db.models.fields.IntegerField', [], {}),
            'duels_won': ('django.db.models.fields.IntegerField', [], {}),
            'duels_won_percentage': ('django.db.models.fields.IntegerField', [], {}),
            'first_yellows': ('django.db.models.fields.IntegerField', [], {}),
            'fouls': ('django.db.models.fields.IntegerField', [], {}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'offsides': ('django.db.models.fields.IntegerField', [], {}),
            'pass_percentage': ('django.db.models.fields.IntegerField', [], {}),
            'possession': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'red_cards': ('django.db.models.fields.IntegerField', [], {}),
            'second_yellows': ('django.db.models.fields.IntegerField', [], {}),
            'shots_off_target': ('django.db.models.fields.IntegerField', [], {}),
            'shots_on_target': ('django.db.models.fields.IntegerField', [], {}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Team']"}),
            'total_passes': ('django.db.models.fields.IntegerField', [], {})
        },
        u'mls_api.substitution': {
            'Meta': {'object_name': 'Substitution'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subbed_in'", 'to': u"orm['mls_api.GamePlayer']"}),
            'minute': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'out_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subbed_out'", 'to': u"orm['mls_api.GamePlayer']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Team']"})
        },
        u'mls_api.team': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Team'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['mls_api']