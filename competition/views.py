import datetime
import operator

from django.db.models import Q

from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *


def index(request):
    all_league = list(LeagueType.objects.all().order_by('name'))
    all_seasons = list(Season.objects.all().order_by('season'))
    context = {
        'all_league': all_league,
        'all_seasons': all_seasons,
    }
    return render(request, 'competition/index.html', context)


def player(request):
    all_players = Player.objects.all()
    context = {'all_players': all_players}
    return render(request, "competition/player.html", context)


def player_details(request, player_id):
    p = get_object_or_404(Player, pk=player_id)
    context = {'player': p}
    return render(request, "competition/player_detail.html", context)


def player_add(request):
    if request.method == 'POST':
        player_form = PlayerForm(data=request.POST)
        if player_form.is_valid():
            new_player = player_form.save(commit=False)
            new_player.save()
            seasons = []
            for league in new_player.team.league.all():
                league_seasons = Season.objects.filter(league=league)
                for season in league_seasons:
                     seasons.append(season)

            for season in seasons:
                player_stats = PlayerStats.create(new_player, season, 0)
                player_stats.save()

        return redirect('competition:player')
    else:
        player_form = PlayerForm()
        return render(request, 'competition/player_add.html', {'player_form': player_form})


def player_delete(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    player.delete()
    return redirect('competition:player')


def player_update(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    player_form = PlayerForm(request.POST or None, instance=player)
    if request.method == 'POST':
        if player_form.is_valid():
            player = player_form.save(commit=False)
            player.save()
            leagues = player.team.league.all()
            player_stats = PlayerStats.objects.filter(player=player)
            new_leagues = [True for i in range(len(leagues))]

            for i, league in enumerate(leagues):
                for stats in player_stats:
                    if stats.season.league == league:
                        new_leagues[i] = False

                if new_leagues[i] == True:
                    seasons = Season.objects.filter(league=league)
                    for season in seasons:
                        new_stats = PlayerStats.create(player, season, 0)
                        new_stats.save()


        return redirect('competition:player')
    return render(request, 'competition/player_add.html', {'player_form': player_form})


def team(request):
    all_teams = Team.objects.all()
    context = {'all_teams': all_teams}
    return render(request, "competition/team.html", context)


def team_details(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    players = Player.objects.filter(team=team_id)
    team_stats = TeamStats.objects.filter(team=team_id)
    leagues = team.league.all()

    season = []
    for league in leagues:
        season += list(Season.objects.filter(league_id=league.id))

    total_goals_scored = 0
    total_goals_lost = 0
    total_matches_won = 0
    total_matches_lost = 0
    total_matches_draw = 0

    if team_stats:
        for stats in team_stats:
            total_goals_scored += stats.goalsScored
            total_goals_lost += stats.goalsLost
            total_matches_won += stats.matchesWon
            total_matches_lost += stats.matchesLost
            total_matches_draw += stats.matchesDraw

    context = {
        'seasons': season,
        'players': players, 'team': team,
        'team_stats': team_stats,
        'total_goals_scored': total_goals_scored,
        'total_goals_lost': total_goals_lost,
        'total_matches_won': total_matches_won,
        'total_matches_lost': total_matches_lost,
        'total_matches_draw': total_matches_draw,
    }
    return render(request, 'competition/team_detail.html', context)


def team_delete(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    matches = Match.objects.filter(Q(host_id=team.id) | Q(guest_id=team.id))
    for match in matches:
        change_stats(match.id, False)
    team.delete()
    return redirect('competition:team')


def team_add(request):
    if request.method == 'POST':
        team_form = TeamForm(request.POST, request.FILES)
        if team_form.is_valid():
            team = team_form.save()
            leagues = team.league.all()
            seasons = []
            for league in leagues:
                seasons += Season.objects.filter(league_id=league.id)
            for season in seasons:
                team_stats = TeamStats.create(team, season)
                team_stats.save()
        else:
            print(team_form.errors)

        return redirect('competition:team')
    else:
        team_form = TeamForm()
        return render(request, 'competition/team_add.html', {'team_form': team_form})


def team_update(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team_form = TeamForm(request.POST or None, instance=team)
    if request.method == 'POST':
        if team_form.is_valid():
            team = team_form.save()
            team_stats = TeamStats.objects.filter(team=team)
            team_leagues = team.league.all()

            if team_stats:
                # arrays that help to indicate valid stats and new leagues
                valid_stats = [False for i in range(len(team_stats))]
                new_leagues = [True for i in range(len(team_leagues))]

                # checking if state is valid (you may delete team from a league but stats stays in db)
                # to prevent bugs in the future, like listing league table within team that is not in the league
                # or listing stats of league that in not team's league
                for league in team_leagues:
                    for i, stats in enumerate(team_stats):
                        if stats.season.league == league:
                            valid_stats[i] = True

                for i, stats in enumerate(team_stats):
                    if not valid_stats[i]:
                        matches = Match.objects.filter(
                            Q(host_id=team.id) | Q(guest_id=team.id),
                            season_id=stats.season.id
                        )
                        for match in matches:
                            change_stats(match.id, False)
                            match.delete()
                        stats.delete()

                # similar to the code above but we're checking if there is a new league that team don't have
                # stats linked to this league
                for stats in team_stats:
                    for i, league in enumerate(team_leagues):
                        if stats.season.league == league:
                            new_leagues[i] = False

                for i, league in enumerate(team_leagues):
                    if new_leagues[i]:
                        seasons = Season.objects.filter(league_id=league.id)
                        for season in seasons:
                            TeamStats.create(team=team, season=season).save()
            # if there is not stats in team linked to leagues we need to create them
            else:
                for league in team_leagues:
                    seasons = Season.objects.filter(league_id=league.id)
                    for season in seasons:
                        TeamStats.create(team=team, season=season).save()

        return redirect('competition:team')
    return render(request, 'competition/team_add.html', {'team_form': team_form})


def league_details(request, league_id):
    teams = Team.objects.filter(league=league_id)
    seasons = Season.objects.filter(league=league_id).order_by('season')
    league = get_object_or_404(LeagueType, pk=league_id)
    context = {
        'teams': teams,
        'league': league,
        'seasons': seasons,
    }
    return render(request, 'competition/league_detail.html', context)


def league_add(request):
    if request.method == 'POST':
        league_form = LeagueForm(data=request.POST)
        if league_form.is_valid():
            new_league = league_form.save(commit=False)
            new_league.save()
        return redirect('competition:index')
    else:
        league_form = LeagueForm()
        return render(request, 'competition/league_add.html', {'league_form': league_form})


def season_add(request, league_id):
    if request.method == 'POST':
        season_form = SeasonForm(data=request.POST)
        if season_form.is_valid():
            season = season_form.save(commit=False)
            league = get_object_or_404(LeagueType, id=league_id)
            season.league = league
            season.save()

            teams = Team.objects.filter(league=season.league)
            for team in teams:
                stats = TeamStats.create(team, season)
                stats.save()


        return redirect('competition:league_details', league_id=league_id)
    else:
        season_form = SeasonForm()
        return render(request, 'competition/season_add.html', {'season_form': season_form})


def league_update(request, league_id):
    league = get_object_or_404(LeagueType, pk=league_id)
    league_form = LeagueForm(request.POST or None, instance=league)
    if request.method == 'POST' and league_form.is_valid():
        league_form.save()
        return redirect('competition:index')
    return render(request, 'competition/league_add.html', {'league_form': league_form})


def league_delete(request, league_id):
    league = get_object_or_404(LeagueType, pk=league_id)
    league.delete()
    return redirect('competition:index')


def match(request):
    matches = Match.objects.all()
    context = {'matches': matches}
    return render(request, 'competition/match.html', context)


def match_details(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    facts = MatchFacts.objects.filter(match=match_id).order_by('minute')
    context = {'match': match, 'facts': facts}
    return render(request, 'competition/match_detail.html', context)


def match_add(request):
    if request.method == 'POST':
        match_form = MatchForm(data=request.POST)
        if match_form.is_valid():
            new_match = match_form.save(commit=False)
            new_match.save()
            change_stats(new_match.id, True)

        return redirect('competition:match')
    else:
        match_form = MatchForm()
        return render(request, 'competition/match_add.html', {'match_form': match_form})


def change_stats(match_id, update):
    new_match = get_object_or_404(Match, id=match_id)
    # if match has been played, if not we don't need to do anything
    if new_match.hostGoals is not None and new_match.guestGoals is not None:
        # working only on stats, not whole teams
        host_stats = get_object_or_404(TeamStats, team_id=new_match.host.id, season_id=new_match.season.id)
        guest_stats = get_object_or_404(TeamStats, team_id=new_match.guest.id, season_id=new_match.season.id)
        goals_host = new_match.hostGoals
        goals_guest = new_match.guestGoals

        if goals_host > goals_guest:
            points_host = 3
            points_guest = 0
        elif goals_host < goals_guest:
            points_host = 0
            points_guest = 3
        else:
            points_host = 1
            points_guest = 1
        # updating stats
        host_stats.addPoints(points=points_host, update=update)
        host_stats.addScoredGoals(goals=goals_host, update=update)
        host_stats.addLostGoals(goals=goals_guest, update=update)
        guest_stats.addPoints(points=points_guest, update=update)
        guest_stats.addScoredGoals(goals=goals_guest, update=update)
        guest_stats.addLostGoals(goals=goals_host, update=update)
        # saving changes
        host_stats.save()
        guest_stats.save()


def match_update(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    match_form = MatchForm(request.POST or None, instance=match)
    if request.method == 'POST' and match_form.is_valid():
        change_stats(match.id, False)
        match = match_form.save()
        change_stats(match.id, True)
        return redirect('competition:match')
    return render(request, 'competition/match_add.html', {'match_form': match_form})


def match_delete(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    change_stats(match.id, False)
    match.delete()
    return redirect('competition:match')


def fact_add(request, match_id):
    if request.method == 'POST':
        fact_form = MatchFactForm(data=request.POST)
        if fact_form.is_valid():
            new_fact = fact_form.save(commit=False)
            new_fact.save()
            if new_fact.incident == 'goal':
                player_stats = get_object_or_404(PlayerStats, player=new_fact.player, season=new_fact.match.season)
                player_stats.addScoredGoals(1, True)
                player_stats.save()
        return redirect('competition:match_details', match_id=match_id)
    else:
        fact_form = MatchFactForm(initial={'match': match_id})
        return render(request, 'competition/fact_add.html', {'fact_form': fact_form})


def fact_delete(request, match_id, fact_id):
    fact = get_object_or_404(MatchFacts, pk=fact_id)
    player_stats = get_object_or_404(PlayerStats, player=fact.player, season=fact.match.season)
    player_stats.addScoredGoals(1, False)
    player_stats.save()
    fact.delete()
    return redirect('competition:match_details', match_id=match_id)


def fact_update(request, match_id, fact_id):
    fact = get_object_or_404(MatchFacts, pk=fact_id)
    fact_form = MatchFactForm(request.POST or None, instance=fact)
    if request.method == 'POST' and fact_form.is_valid():
        fact_form.save()
        return redirect('competition:match_details', match_id=match_id)
    else:
        return render(request, 'competition/fact_add.html', {'fact_form': fact_form})


def league_seasons(request, league_id):
    league = get_object_or_404(LeagueType, id=league_id)
    seasons = Season.objects.filter(league_id=league_id).order_by('season')
    context = {
        'league': league,
        'seasons': seasons,
    }
    return render(request, 'competition/league_seasons.html', context)


def season_table(request, league_id, season_id):
    season = get_object_or_404(Season, id=season_id)
    team_stats = TeamStats.objects.filter(season_id=season_id).order_by('-scores')
    all_stats = list(PlayerStats.objects.filter(season=season).order_by('-goalsScored'))

    if len(all_stats) > 3:
        stats = all_stats[0:3]
    else:
        stats = all_stats

    context = {
        'team_stats': team_stats,
        'season': season,
        'stats': stats,
    }
    return render(request, 'competition/season_table.html', context)
































