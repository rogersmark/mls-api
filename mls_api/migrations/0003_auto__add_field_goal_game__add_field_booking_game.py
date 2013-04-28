# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Goal.game'
        db.add_column(u'mls_api_goal', 'game',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['mls_api.Game']),
                      keep_default=False)

        # Adding field 'Booking.game'
        db.add_column(u'mls_api_booking', 'game',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['mls_api.Game']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Goal.game'
        db.delete_column(u'mls_api_goal', 'game_id')

        # Deleting field 'Booking.game'
        db.delete_column(u'mls_api_booking', 'game_id')


    models = {
        u'mls_api.booking': {
            'Meta': {'object_name': 'Booking'},
            'card_color': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mls_api.Game']"}),
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