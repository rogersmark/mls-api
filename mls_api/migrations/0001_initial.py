# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Team'
        db.create_table(u'mls_api_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'mls_api', ['Team'])

        # Adding model 'Player'
        db.create_table(u'mls_api_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mls_api.Team'])),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'mls_api', ['Player'])

        # Adding model 'GamePlayer'
        db.create_table(u'mls_api_gameplayer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mls_api.Player'])),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mls_api.Game'])),
            ('captain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mls_api.Team'])),
        ))
        db.send_create_signal(u'mls_api', ['GamePlayer'])

        # Adding model 'Competition'
        db.create_table(u'mls_api_competition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal(u'mls_api', ['Competition'])

        # Adding model 'Game'
        db.create_table(u'mls_api_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('home_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='home_team', to=orm['mls_api.Team'])),
            ('away_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='away_team', to=orm['mls_api.Team'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('home_score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('away_score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mls_api.Competition'])),
            ('stat_link', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal(u'mls_api', ['Game'])

        # Adding model 'Substitution'
        db.create_table(u'mls_api_substitution', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('out_player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subbed_out', to=orm['mls_api.Player'])),
            ('in_player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subbed_in', to=orm['mls_api.Player'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mls_api.Team'])),
            ('minute', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'mls_api', ['Substitution'])

        # Adding model 'Goal'
        db.create_table(u'mls_api_goal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('minute', self.gf('django.db.models.fields.IntegerField')()),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mls_api.GamePlayer'])),
            ('penalty', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'mls_api', ['Goal'])

        # Adding M2M table for field assisted_by on 'Goal'
        db.create_table(u'mls_api_goal_assisted_by', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('goal', models.ForeignKey(orm[u'mls_api.goal'], null=False)),
            ('gameplayer', models.ForeignKey(orm[u'mls_api.gameplayer'], null=False))
        ))
        db.create_unique(u'mls_api_goal_assisted_by', ['goal_id', 'gameplayer_id'])

        # Adding model 'Booking'
        db.create_table(u'mls_api_booking', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('minute', self.gf('django.db.models.fields.IntegerField')()),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mls_api.Player'])),
            ('card_color', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal(u'mls_api', ['Booking'])


    def backwards(self, orm):
        # Deleting model 'Team'
        db.delete_table(u'mls_api_team')

        # Deleting model 'Player'
        db.delete_table(u'mls_api_player')

        # Deleting model 'GamePlayer'
        db.delete_table(u'mls_api_gameplayer')

        # Deleting model 'Competition'
        db.delete_table(u'mls_api_competition')

        # Deleting model 'Game'
        db.delete_table(u'mls_api_game')

        # Deleting model 'Substitution'
        db.delete_table(u'mls_api_substitution')

        # Deleting model 'Goal'
        db.delete_table(u'mls_api_goal')

        # Removing M2M table for field assisted_by on 'Goal'
        db.delete_table('mls_api_goal_assisted_by')

        # Deleting model 'Booking'
        db.delete_table(u'mls_api_booking')


    models = {
        u'mls_api.booking': {
            'Meta': {'object_name': 'Booking'},
            'card_color': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minute': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Player']"})
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
        u'mls_api.game': {
            'Meta': {'object_name': 'Game'},
            'away_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_team'", 'to': u"orm['mls_api.Team']"}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Competition']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'home_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_team'", 'to': u"orm['mls_api.Team']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['mls_api.Player']", 'through': u"orm['mls_api.GamePlayer']", 'symmetrical': 'False'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minute': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'penalty': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.GamePlayer']"})
        },
        u'mls_api.player': {
            'Meta': {'object_name': 'Player'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Team']"})
        },
        u'mls_api.substitution': {
            'Meta': {'object_name': 'Substitution'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subbed_in'", 'to': u"orm['mls_api.Player']"}),
            'minute': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'out_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subbed_out'", 'to': u"orm['mls_api.Player']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Team']"})
        },
        u'mls_api.team': {
            'Meta': {'object_name': 'Team'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['mls_api']