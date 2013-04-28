import os
from mock import Mock
from datetime import datetime

from django.test import TestCase

from mls_scraper import mls_scraper
from mls_api import models
from mls_api.management.commands import scrape_game


class TestScrapeGame(TestCase):
    ''' Test scrape_game management command '''

    def setUp(self):
        super(TestScrapeGame, self).setUp()
        self.orig_requests = mls_scraper.requests
        self.stat_html = open(
            os.path.join(os.path.dirname(__file__), 'test_stats.html')
        ).read()
        mls_scraper.requests = Mock()
        self.game = mls_scraper.GameStatSet()
        self.command = scrape_game.Command()
        self.command.force = False
        self.command.stderr = Mock()
        self.command.stdout = Mock()
        self.competition = models.Competition.objects.get(slug='mls-2013')

    def tearDown(self):
        mls_scraper.requests = self.orig_requests
        super(TestScrapeGame, self).tearDown()

    def _create_requests_mock_return(self, url='http://www.example.com/stats',
                                     status_code=200):
        requests_mock = Mock()
        requests_mock.get.return_value = Mock(
            content=self.stat_html,
            status_code=status_code,
            url=url,
        )
        mls_scraper.requests = requests_mock

    def _init_game_stats(self):
        self.command.game = models.Game(
            competition=self.competition,
            stat_link='http://www.example.com/stats',
            start_time=datetime.now()
        )
        self.command.parsed_stats = mls_scraper.GameStatSet(
            'http://www.example.com/stats')

    def test_parse_game_stats(self):
        ''' Test the main engine behind the scraper tool '''
        methods_to_mock = [
            '_handle_teams',
            '_handle_players',
            '_handle_goals',
            '_handle_bookings',
            '_handle_team_stats',
        ]
        assert methods_to_mock

    def test_handle_teams(self):
        ''' Test the _handle_teams methods '''
        self._create_requests_mock_return()
        self._init_game_stats()
        self.command._handle_teams()
        self.assertEqual(
            self.command.game.home_team,
            models.Team.objects.get(name='Chicago Fire')
        )
        self.assertEqual(
            self.command.game.away_team,
            models.Team.objects.get(name='Chivas USA')
        )

    def test_handle_players(self):
        ''' Test the creation of player objects in _handle_players '''
        self._create_requests_mock_return()
        self._init_game_stats()
        self.command._handle_teams()
        self.command.game.save()
        self.command._handle_players(
            self.command.parsed_stats.home_team,
            self.command.game.home_team
        )
        self.assertEqual(
            models.Player.objects.count(),
            14
        )

    def test_handle_goals(self):
        ''' Tests the functionality of handling goals in the scraper '''
        self._create_requests_mock_return()
        self._init_game_stats()
        self.command._handle_teams()
        self.command.game.save()
        self.command._handle_players(
            self.command.parsed_stats.home_team,
            self.command.game.home_team
        )
        self.command._handle_players(
            self.command.parsed_stats.away_team,
            self.command.game.away_team
        )
        self.command._handle_goals()
        self.assertEqual(
            models.Goal.objects.count(),
            5
        )

    def test_handle_bookings(self):
        ''' Test handling the creation of booking events '''
        self._create_requests_mock_return()
        self._init_game_stats()
        self.command._handle_teams()
        self.command.game.save()
        self.command._handle_players(
            self.command.parsed_stats.home_team,
            self.command.game.home_team
        )
        self.command._handle_players(
            self.command.parsed_stats.away_team,
            self.command.game.away_team
        )
        self.command._handle_bookings()
        self.assertEqual(
            models.Booking.objects.count(),
            3
        )

    def test_handle_team_stats(self):
        ''' Test the handling of creating team stats '''
        self._create_requests_mock_return()
        self._init_game_stats()
        self.command._handle_teams()
        self.command.game.save()
        self.command._handle_players(
            self.command.parsed_stats.home_team,
            self.command.game.home_team
        )
        self.command._handle_players(
            self.command.parsed_stats.away_team,
            self.command.game.away_team
        )
        self.command._handle_team_stats()
        self.assertEqual(
            models.StatSet.objects.count(),
            2
        )
        self.assertEqual(
            models.StatSet.objects.filter(team__name='Chicago Fire').count(),
            1
        )
        self.assertEqual(
            models.StatSet.objects.get(team__name='Chicago Fire').shots_on_target,
            8
        )
