import os
import logging
from mock import Mock
from datetime import datetime

from django.test import TestCase
from django.core.management.base import CommandError

from mls_scraper import parser as mls_parser
from mls_api import models
from mls_api.management.commands import scrape_game


class TestScrapeGame(TestCase):
    ''' Test scrape_game management command '''

    def setUp(self):
        super(TestScrapeGame, self).setUp()
        self.orig_requests = mls_parser.requests
        self.orig_cmd_requests = scrape_game.requests
        scrape_game.requests = Mock()
        self.stat_html = open(
            os.path.join(os.path.dirname(__file__), 'test_stats.html')
        ).read()
        self.formation_html = open(
            os.path.join(os.path.dirname(__file__), 'test_formation.html')
        ).read()
        mls_parser.requests = Mock()
        self.command = scrape_game.Command()
        self.command.logger = logging.getLogger('testing')
        self.command.force = False
        self.command.stderr = Mock()
        self.command.stdout = Mock()
        self.competition = models.Competition.objects.get(slug='mls-2013')

    def tearDown(self):
        mls_parser.requests = self.orig_requests
        scrape_game.requests = self.orig_cmd_requests
        super(TestScrapeGame, self).tearDown()

    def _create_requests_mock_return(self, url='http://www.example.com/stats',
                                     status_code=200,
                                     html=None,
                                     cmd_req=False):
        requests_mock = Mock()
        game_mock = Mock(
            content=html if html else self.stat_html,
            status_code=status_code,
            url=url
        )
        formation_mock = Mock(
            content=self.formation_html,
            status_code=status_code,
            url=url
        )
        requests_mock.get.side_effect = [
            game_mock,
            formation_mock
        ]
        if cmd_req:
            scrape_game.requests = requests_mock
        else:
            mls_parser.requests = requests_mock

    def _init_game_stats(self, force=True, year=2013):
        threaded_parser = scrape_game.ThreadedGameParser(
            force=True,
            logger=Mock(),
            year=2013,
            queue=Mock()
        )
        threaded_parser.game = models.Game(
            competition=self.competition,
            stat_link='http://www.example.com/stats',
            start_time=datetime.now()
        )
        threaded_parser.parsed_stats = mls_parser.MLSStatsParser(
            'http://www.example.com/stats')
        return threaded_parser

    def test_parse_game_stats(self):
        ''' Test the main engine behind the scraper tool '''
        self._create_requests_mock_return()
        parser = scrape_game.ThreadedGameParser(
            force=True,
            logger=Mock(),
            year=2013,
            queue=Mock()
        )
        methods_to_mock = [
            '_handle_players',
            '_handle_goals',
            '_handle_bookings',
            '_handle_team_stats',
            '_handle_formations',
            '_handle_subs',
            '_handle_result',
        ]
        assert methods_to_mock
        pre_mocks = []
        for method in methods_to_mock:
            pre_mocks.append(getattr(parser, method))
            setattr(parser, method, Mock())

        parser._parse_game_stats('http://www.exmaple.com/stats')
        for count, method in enumerate(methods_to_mock):
            assert getattr(parser, method).called
            setattr(parser, method, pre_mocks[count])

    def test_handle_teams(self):
        ''' Test the _handle_teams methods '''
        self._create_requests_mock_return()
        parser = self._init_game_stats()
        parser.game.save()
        parser._handle_teams()
        self.assertEqual(
            parser.game.home_team.team,
            models.Team.objects.get(name='Chicago Fire')
        )
        self.assertEqual(
            parser.game.away_team.team,
            models.Team.objects.get(name='Chivas USA')
        )

    def test_handle_players(self):
        ''' Test the creation of player objects in _handle_players '''
        self._create_requests_mock_return()
        parser = self._init_game_stats()
        parser.game.save()
        parser._handle_teams()
        parser.game.save()
        parser._handle_players(
            parser.parsed_stats.game.home_team,
            parser.game.home_team.team
        )
        self.assertEqual(
            models.Player.objects.count(),
            14
        )
        self.assertEqual(
            models.GamePlayer.objects.count(),
            14
        )
        self.assertEqual(
            models.PlayerStatLine.objects.count(),
            14
        )

    def test_handle_goals(self):
        ''' Tests the functionality of handling goals in the scraper '''
        self._create_requests_mock_return()
        parser = self._init_game_stats()
        parser.game.save()
        parser._handle_teams()
        parser.game.save()
        parser._handle_players(
            parser.parsed_stats.game.home_team,
            parser.game.home_team.team
        )
        parser._handle_players(
            parser.parsed_stats.game.away_team,
            parser.game.away_team.team
        )
        parser._handle_goals()
        self.assertEqual(
            models.Goal.objects.count(),
            5
        )

    def test_handle_bookings(self):
        ''' Test handling the creation of booking events '''
        self._create_requests_mock_return()
        parser = self._init_game_stats()
        parser.game.save()
        parser._handle_teams()
        parser.game.save()
        parser._handle_players(
            parser.parsed_stats.game.home_team,
            parser.game.home_team.team
        )
        parser._handle_players(
            parser.parsed_stats.game.away_team,
            parser.game.away_team.team
        )
        parser._handle_bookings()
        self.assertEqual(
            models.Booking.objects.count(),
            3
        )

    def test_handle_subs(self):
        ''' Test handling the creation of substitution events '''
        self._create_requests_mock_return()
        parser = self._init_game_stats()
        parser.game.save()
        parser._handle_teams()
        parser.game.save()
        parser._handle_players(
            parser.parsed_stats.game.home_team,
            parser.game.home_team.team
        )
        parser._handle_players(
            parser.parsed_stats.game.away_team,
            parser.game.away_team.team
        )
        parser._handle_subs()
        self.assertEqual(
            models.Substitution.objects.filter(
                team=parser.game.home_team).count(),
            3
        )
        self.assertEqual(
            models.Substitution.objects.filter(
                team=parser.game.away_team).count(),
            3
        )

    def test_handle_team_stats(self):
        ''' Test the handling of creating team stats '''
        self._create_requests_mock_return()
        parser = self._init_game_stats()
        parser.game.save()
        parser._handle_teams()
        parser.game.save()
        parser._handle_players(
            parser.parsed_stats.game.home_team,
            parser.game.home_team.team
        )
        parser._handle_players(
            parser.parsed_stats.game.away_team,
            parser.game.away_team.team
        )
        parser._handle_team_stats()
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

    def test_handle(self):
        ''' Test the functionality of the main entry point, Command.handle '''
        self.command._parse_game_stats = Mock()
        self.command._find_urls = Mock()
        self.command._find_urls.return_value = [1, 2, 3]
        self.command.handle()
        self.assertEqual(self.command.urls, [1, 2, 3])
        self.assertEqual(self.command.year, 2013)
        self.assertEqual(self.command.force, False)

    def test_handle_invalid_year(self):
        ''' Test handle with an invalid year '''
        self.command._parse_game_stats = Mock()
        self.command._find_urls = Mock()
        self.command._find_urls.return_value = [1, 2, 3]
        with self.assertRaises(CommandError):
            self.command.handle(year='2014')

    def test_handle_provided_urls(self):
        ''' Test handle with urls provided from the command line '''
        self.command._parse_game_stats = Mock()
        self.command._find_urls = Mock()
        self.command._find_urls.return_value = [1, 2, 3]
        self.command.handle('link1', 'link2')
        self.assertEqual(self.command.urls, ('link1', 'link2'))

    def test_find_urls(self):
        ''' Tests the find urls functionality of scrape_game '''
        html = open(
            os.path.join(os.path.dirname(__file__), 'results_map.html')
        ).read()
        self._create_requests_mock_return(html=html, cmd_req=True)
        self.command.year = 2013
        links = self.command._find_urls()
        assert links
        # HTML dump we have has 77 stats links in it
        self.assertEqual(len(links), 77)

    def test_handle_formations(self):
        ''' Test the formation creation functionality '''
        self._create_requests_mock_return()
        parser = scrape_game.ThreadedGameParser(
            force=True,
            year=2013,
            logger=Mock(),
            queue=Mock()
        )
        parser._parse_game_stats('http://www.exmaple.com/stats')
        self.assertEqual(models.Formation.objects.count(), 2)
        fire_formation = models.Formation.objects.get(
            team__slug='chicago-fire')
        self.assertEqual(fire_formation.formation_str, '4-2-3-1')

    def test_handle_result(self):
        self._create_requests_mock_return()
        parser = self._init_game_stats()
        parser.game.save()
        parser._handle_teams()
        parser.game.save()
        parser._handle_players(
            parser.parsed_stats.game.home_team,
            parser.game.home_team.team
        )
        parser._handle_players(
            parser.parsed_stats.game.away_team,
            parser.game.away_team.team
        )
        parser._handle_goals()
        parser._handle_result()
        self.assertEqual(
            parser.game.home_team.result,
            models.Result.objects.get(code=models.Result.LOSS)
        )
        self.assertEqual(
            parser.game.away_team.result,
            models.Result.objects.get(code=models.Result.WIN)
        )
        self.assertEqual(
            parser.game.home_score,
            1
        )
        self.assertEqual(
            parser.game.away_score,
            4
        )
