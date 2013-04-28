import re
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify

from mls_scraper.mls_scraper import GameStatSet
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
    )

    def handle(self, *args, **options):
        if not args:
            raise CommandError('Command requires a link to post game stats')
        self.force = options['force'] if options['force'] else False
        failed_urls = []
        for url in args:
            self.stdout.write('Scraping %s.' % url)
            try:
                self._parse_game_stats(url)
            except Exception as e:
                failed_urls.append(url)
                self.stdout.write('Failed to scrape %s.' % url)
                print e
            else:
                self.stdout.write('Completed scraping %s.' % url)

        if failed_urls:
            self.stderr.write('Failures: ')
            for url in failed_urls:
                self.stderr.write(url)

    def _get_parsed_name(self, name):
        ''' Takes a player name and generates first/last names '''
        player_name = name.split()
        first_name = ''
        last_name = ''
        if len(player_name) == 1:
            first_name = last_name = player_name[0]
        else:
            first_name = player_name[0]
            last_name = player_name[1]

        return first_name, last_name

    def _parse_game_stats(self, url):
        ''' Engine of this operation '''
        if self.force:
            models.Game.objects.filter(stat_link=url).delete()
        elif models.Game.objects.filter(stat_link=url).exists():
            self.stderr.write('Game already exists, skipping')
            return

        try:
            self.parsed_stats = GameStatSet(url)
        except:
            self.stderr.write('Failed to parse')
            raise

        competition, created = models.Competition.objects.get_or_create(
            name='MLS 2013', slug='mls-2013', year='2013')
        self.game = models.Game(
            stat_link=url,
            competition=competition,
            start_time=self.parsed_stats.game_date
        )
        self._handle_teams()
        self.game.save()
        self._handle_players(
            self.parsed_stats.home_team,
            self.game.home_team
        )
        self._handle_players(
            self.parsed_stats.away_team,
            self.game.away_team
        )
        self.game.save()
        self._handle_goals()
        self.game.save()
        self._handle_bookings()
        self.game.save()
        self._handle_team_stats()
        self.game.save()

    def _handle_teams(self):
        home_team, created = models.Team.objects.get_or_create(
            name=self.parsed_stats.home_team.name,
            slug=slugify(self.parsed_stats.home_team.name)
        )
        away_team, created = models.Team.objects.get_or_create(
            name=self.parsed_stats.away_team.name,
            slug=slugify(self.parsed_stats.away_team.name)
        )
        self.game.home_team = home_team
        self.game.away_team = away_team

    def _handle_players(self, team_stats, team):
        for player in team_stats.players + team_stats.keepers:
            first_name, last_name = self._get_parsed_name(
                player['Player'])
            player_obj, created = models.Player.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                team=team,
                number=player['#'],
                defaults={'position': player.get('POS', 'S')}
            )
            models.GamePlayer.objects.get_or_create(
                game=self.game,
                team=team,
                player=player_obj,
                position=player.get('POS', 'S')
            )

    def _handle_goals(self):
        ''' Parse goal events '''
        for goal in self.parsed_stats.goals:
            team = models.Team.objects.get(
                name=GameStatSet.abbreviation_map[goal['Club']]
            )
            first_name, last_name = self._get_parsed_name(
                goal['Player'])
            player = models.Player.objects.get(
                first_name=first_name,
                last_name=last_name,
                team=team
            )
            gp = models.GamePlayer.objects.get(
                player=player,
                game=self.game,
                team=team
            )
            goal_obj, created = models.Goal.objects.get_or_create(
                minute=re.search('\d+', goal['Time']).group(),
                game=self.game,
                player=gp,
                own_goal=True if re.search('(OG)', goal['Player']) else False
            )
            assists = goal.get(
                '(Assisted by)', '').lstrip('(').rstrip(')').split(',')
            if assists == ['']:
                assists = []
            for assist in assists:
                first_name, last_name = self._get_parsed_name(assist)
                player = models.Player.objects.get(
                    first_name=first_name,
                    last_name=last_name,
                    team=team
                )
                gp = models.GamePlayer.objects.get(
                    player=player,
                    game=self.game,
                    team=team
                )
                goal_obj.assisted_by.add(gp)
                goal_obj.save()

    def _handle_bookings(self):
        ''' Handle any bookings that occur in a match '''
        for booking in self.parsed_stats.disciplinary_events:
            team = models.Team.objects.get(
                name=GameStatSet.abbreviation_map[booking['Club']]
            )
            first_name, last_name = self._get_parsed_name(
                booking['Player'])
            player = models.Player.objects.get(
                first_name=first_name,
                last_name=last_name,
                team=team
            )
            gp = models.GamePlayer.objects.get(
                player=player,
                game=self.game,
                team=team
            )
            booking_obj, created = models.Booking.objects.get_or_create(
                minute=re.search('\d+', booking['Time']).group(),
                game=self.game,
                player=gp,
                reason=booking['Reason'],
                card_color=booking['card_color'],
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
            self.game.home_team,
            self.parsed_stats.home_team.stats
        )
        self._parse_team_stats(
            self.game.away_team,
            self.parsed_stats.away_team.stats
        )
