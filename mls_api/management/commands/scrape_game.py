import logging
import Queue
import threading
from optparse import make_option
from datetime import datetime

import requests
from BeautifulSoup import BeautifulSoup

from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify

from mls_scraper import parser
from mls_api import models


class Command(BaseCommand):
    args = '<http://mlssoccer.com/stat_link http://mls... >'
    help = 'Scrapes the stats for a given game link and stores the results'
    option_list = BaseCommand.option_list + (
        make_option(
            '-f', '--force',
            action='store_true',
            dest='force',
            help='With force, will overwrite any currently stored game data'
        ),
        make_option(
            '-y', '--year',
            dest='year',
            help='The year of the MLS season you wish to parse',
            default='2013',
        ),
        make_option(
            '-w', '--workers',
            dest='workers',
            help='Number of threads to scrape with (Be careful!)',
            default=5
        ),
    )

    def _find_urls(self):
        ''' Finds result URLs from http://www.mlssoccer.com/results/ '''
        resp = requests.get(
            'http://www.mlssoccer.com/results/%s' % self.year)
        content = BeautifulSoup(resp.content)
        stats = content.findAll('div', {'class': 'stats-table'})[0]
        table = stats.findChildren('table')[0]
        links = table.findChildren('a')
        valid_links = []
        for link in links:
            if link.parent.attrs[0][1] == 'notplayed':
                # Skip unplayed games
                continue
            href = '%s/stats' % link.attrs[-1][-1]
            if href not in valid_links:
                valid_links.append(href)

        return valid_links

    def handle(self, *args, **options):
        self.logger = logging.getLogger('scraper')
        self.force = options['force'] if options.get('force') else False
        self.year = options.get('year', 2013)
        self.workers = int(options.get('workers', 5))
        if int(self.year) > datetime.now().year or int(self.year) < 2011:
            raise CommandError('Invalid Year')
        self.urls = args
        if not self.urls:
            self.urls = self._find_urls()
        failed_urls = []
        queue = Queue.Queue()
        for url in self.urls:
            queue.put(url)

        self.stdout.write('Starting scraper of %d matches' % queue.qsize())
        while not queue.empty():
            active_workers = self.workers if queue.qsize() > self.workers else queue.qsize()
            threads = []
            for x in range(active_workers):
                t = ThreadedGameParser(
                    self.year, self.force, self.logger, queue
                )
                t.setDaemon(True)
                t.start()
                threads.append(t)

            while threads:
                active_threads = []
                for thread in threads:
                    if thread.isAlive():
                        active_threads.append(thread)
                threads = active_threads

            self.logger.info(
                '%s of %s jobs completed' % (
                    len(self.urls) - queue.qsize(),
                    len(self.urls)
                )
            )

        self.stdout.write('Finished scraper')
        if failed_urls:
            self.stderr.write('Failures: ')
            for url in failed_urls:
                self.stderr.write(url)


class ThreadedGameParser(threading.Thread):

    def __init__(self, year, force, logger, queue):
        super(ThreadedGameParser, self).__init__()
        self.year = year
        self.force = force
        self.logger = logger
        self.queue = queue
        self.url = self.queue.get()

    def run(self):
        self.logger.info('Parsing %s', self.url)
        try:
            self._parse_game_stats(self.url)
        except:
            self.logger.exception('Failed to scrape %s.', self.url)
        else:
            self.logger.info('Finished parsing %s', self.url)
        self.queue.task_done()

    def _parse_game_stats(self, url):
        ''' Engine of this operation '''
        if self.force:
            # FYI, this will cascade and take a lot of stuff with it.
            models.Game.objects.filter(stat_link=url).delete()
        elif models.Game.objects.filter(stat_link=url).exists():
            self.logger.error('Game %s already exists, skipping', url)
            return

        try:
            self.parsed_stats = parser.MLSStatsParser(url, logger=self.logger)
        except:
            self.logger.exception('Failed to parse %s.', url)
            return

        competition, created = models.Competition.objects.get_or_create(
            name='MLS %s' % self.year,
            slug='mls-%s' % self.year,
            year=self.year)
        self.game = models.Game(
            stat_link=url,
            competition=competition,
            start_time=self.parsed_stats.game.game_date
        )
        self.game.save()
        self._handle_teams()
        self.game.save()
        self._handle_players(
            self.parsed_stats.game.home_team,
            self.game.home_team.team
        )
        self._handle_players(
            self.parsed_stats.game.away_team,
            self.game.away_team.team
        )
        self.game.save()
        self._handle_goals()
        self.game.save()
        self._handle_bookings()
        self.game.save()
        self._handle_subs()
        self.game.save()
        self._handle_team_stats()
        self.game.save()
        self._handle_formations()
        self.game.save()
        self._handle_result()
        self.game.save()

    def _handle_teams(self):
        home_team, created = models.Team.objects.get_or_create(
            name=self.parsed_stats.game.home_team.name,
            slug=slugify(self.parsed_stats.game.home_team.name)
        )
        away_team, created = models.Team.objects.get_or_create(
            name=self.parsed_stats.game.away_team.name,
            slug=slugify(self.parsed_stats.game.away_team.name)
        )
        models.GameTeam.objects.create(
            game=self.game,
            team=home_team,
            home=True
        )
        models.GameTeam.objects.create(
            game=self.game,
            team=away_team,
            home=False
        )

    def _handle_players(self, team_stats, team):
        for player in team_stats.players:
            player_obj, created = models.Player.objects.get_or_create(
                first_name=player.first_name,
                last_name=player.last_name,
                team=team,
                defaults={
                    'position': player.position,
                    'number': player.number
                }
            )
            gp, created = models.GamePlayer.objects.get_or_create(
                game=self.game,
                team=team,
                player=player_obj,
                position=player.position,
            )
            # Feel bad about all the getattrs, but the Player objects
            # coming in can be a bit unpredictable
            models.PlayerStatLine.objects.get_or_create(
                player=gp,
                shots=getattr(player, 'shots', 0),
                shots_on_goal=getattr(player, 'shots_on_goal', 0),
                minutes=getattr(player, 'minutes', 0),
                goals=getattr(player, 'goals', 0),
                assists=getattr(player, 'assists', 0),
                fouls_commited=getattr(player, 'fouls_commited', 0),
                fouls_suffered=getattr(player, 'fouls_suffered', 0),
                corners=getattr(player, 'corners', 0),
                offsides=getattr(player, 'offsides', 0),
                saves=getattr(player, 'saves', 0),
                goals_against=getattr(player, 'goals_against', 0)
            )

    def _handle_goals(self):
        ''' Parse goal events '''
        for goal in self.parsed_stats.game.goals:
            team = models.Team.objects.get(
                name=goal.team.name
            )
            player = models.Player.objects.get(
                first_name=goal.player.first_name,
                last_name=goal.player.last_name,
                team=team
            )
            gp = models.GamePlayer.objects.get(
                player=player,
                game=self.game,
                team=team
            )
            goal_obj, created = models.Goal.objects.get_or_create(
                minute=goal.time,
                game=self.game,
                player=gp,
                own_goal=goal.own_goal
            )
            for assist in goal.assisted_by:
                player = models.Player.objects.get(
                    first_name=assist.first_name,
                    last_name=assist.last_name,
                    team=team
                )
                gp = models.GamePlayer.objects.get(
                    player=player,
                    game=self.game,
                    team=team
                )
                goal_obj.assisted_by.add(gp)
                goal_obj.save()

        self.game.home_score = self.game._home_score
        self.game.away_score = self.game._away_score
        self.game.save()

    def _handle_bookings(self):
        ''' Handle any bookings that occur in a match '''
        for booking in self.parsed_stats.game.disciplinary_events:
            team = models.Team.objects.get(
                name=booking.team.name
            )
            player = models.Player.objects.get(
                first_name=booking.player.first_name,
                last_name=booking.player.last_name,
                team=team
            )
            gp = models.GamePlayer.objects.get(
                player=player,
                game=self.game,
                team=team
            )
            booking_obj, created = models.Booking.objects.get_or_create(
                minute=booking.time,
                game=self.game,
                player=gp,
                reason=booking.reason,
                card_color=booking.card_color,
            )

    def _handle_subs(self):
        ''' Handle sub events from a match '''
        for sub_event in self.parsed_stats.game.subs:
            team = models.Team.objects.get(
                name=sub_event.team.name
            )

            player_on = models.Player.objects.get(
                first_name=sub_event.player_on.first_name,
                last_name=sub_event.player_on.last_name,
                team=team
            )
            gp_on = models.GamePlayer.objects.get(
                player=player_on,
                game=self.game,
                team=team
            )

            player_off = models.Player.objects.get(
                first_name=sub_event.player_off.first_name,
                last_name=sub_event.player_off.last_name,
                team=team
            )
            gp_off = models.GamePlayer.objects.get(
                player=player_off,
                game=self.game,
                team=team
            )

            substitution, created = models.Substitution.objects.get_or_create(
                team=team,
                in_player=gp_on,
                out_player=gp_off,
                minute=sub_event.time
            )

    def _parse_team_stats(self, team_obj, team_stats):
        ''' Team agnostic method of handling the stats '''
        stat_set, created = models.StatSet.objects.get_or_create(
            team=team_obj,
            game=self.game,
            attempts_on_goal=team_stats['Attempts on Goal'],
            shots_on_target=team_stats['Shots on Target'],
            shots_off_target=team_stats['Shots off Target'],
            blocked_shots=team_stats['Blocked Shots'],
            corner_kicks=team_stats['Corner Kicks'],
            fouls=team_stats['Fouls'],
            crosses=team_stats['Open Play Crosses'],
            offsides=team_stats['Offsides'],
            first_yellows=team_stats['First Yellow Cards'],
            second_yellows=team_stats['Second Yellow Cards'],
            red_cards=team_stats['Red Cards'],
            duels_won=team_stats['Duels Won'],
            duels_won_percentage=team_stats['Duels Won %'].rstrip('%'),
            total_passes=team_stats['Total Pass'],
            pass_percentage=team_stats['Passing Accuracy %'].rstrip('%'),
            possession=team_stats['Possession'].rstrip('%'),
        )

    def _handle_team_stats(self):
        ''' Handle all of the creation of StatSet objects '''
        self._parse_team_stats(
            self.game.home_team.team,
            self.parsed_stats.game.home_team.stats
        )
        self._parse_team_stats(
            self.game.away_team.team,
            self.parsed_stats.game.away_team.stats
        )

    def _parse_formations(self, team, formation):
        ''' Helper for creating the formation objects '''
        formation_obj = models.Formation.objects.create(
            game=self.game,
            team=team
        )
        for count, line in enumerate(formation.players):
            form_line = models.FormationLine.objects.create(
                formation=formation_obj,
                sort_order=count,
            )
            for inner_count, player in enumerate(line):
                player = models.Player.objects.get(
                    first_name=player.first_name,
                    last_name=player.last_name,
                    team=team
                )
                gp = models.GamePlayer.objects.get(
                    player=player,
                    game=self.game,
                    team=team
                )
                models.FormationPlayer.objects.create(
                    player=gp,
                    line=form_line,
                    sort_order=inner_count
                )

    def _handle_formations(self):
        ''' Handles creating the formations for the match '''
        self._parse_formations(
            self.game.home_team.team,
            self.parsed_stats.game.home_team.formation
        )
        self._parse_formations(
            self.game.away_team.team,
            self.parsed_stats.game.away_team.formation
        )

    def _handle_result(self):
        ''' Handle filling out the results '''
        win = models.Result.objects.get(code=models.Result.WIN)
        draw = models.Result.objects.get(code=models.Result.DRAW)
        loss = models.Result.objects.get(code=models.Result.LOSS)
        home_team = self.game.home_team
        away_team = self.game.away_team
        if self.game.home_score > self.game.away_score:
            home_team.result = win
            away_team.result = loss
        elif self.game.away_score > self.game.home_score:
            home_team.result = loss
            away_team.result = win
        elif self.game.home_score == self.game.away_score:
            home_team.result = away_team.result = draw

        home_team.save()
        away_team.save()
