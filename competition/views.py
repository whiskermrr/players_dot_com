import datetime

from .models import LeagueType, Team, Match, Kolejka, Table, Player, MatchFacts
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PlayerForm, LeagueForm, MatchForm, TeamForm, MatchFactForm


def index(request):
    all_league = list(LeagueType.objects.all().order_by('name'))
    for row in all_league:
        count = 0
        for row2 in all_league:
            if row.name == row2.name:
                count += 1
                if count > 1:
                    all_league.remove(row)
    context = {'all_league': all_league}
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
            player_form.save()
        return redirect('competition:player')
    return render(request, 'competition/player_add.html', {'player_form': player_form})


def team(request):
    all_teams = Team.objects.all()
    context = {'all_teams': all_teams}
    return render(request, "competition/team.html", context)


def team_details(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    players = Player.objects.filter(team=team_id)
    context = {'players': players, 'team': team}
    return render(request, 'competition/team_detail.html', context)


def team_delete(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team.delete()
    return redirect('competition:team')


def team_add(request):
    if request.method == 'POST':
        team_form = TeamForm(data=request.POST)
        if team_form.is_valid():
            team_form.save()
        return redirect('competition:team')
    else:
        team_form = TeamForm()
        return render(request, 'competition/team_add.html', {'team_form': team_form})


def team_update(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team_form = TeamForm(request.POST or None, instance=team)
    if request.method == 'POST':
        if team_form.is_valid():
            team_form.save()
        return redirect('competition:team')
    return render(request, 'competition/team_add.html', {'team_form': team_form})


def league_details(request, league_id):
    teams = Team.objects.filter(league=league_id)
    league = get_object_or_404(LeagueType, pk=league_id)
    context = {'teams': teams, 'league': league}
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


def league_seasons(request, league_name):

    seasons = LeagueType.objects.filter(name=league_name)
    return render(request, 'competition/league_seasons.html', {'seasons': seasons, 'league_name': league_name})


def season_teams(request, league_name, league_id):
    # Kolejka.objects.all().delete()
    # Match.objects.all().delete()

    teams = list(Team.objects.filter(league__id=league_id))
    league = LeagueType.objects.filter(pk=league_id).first()
    kolejki = list(Kolejka.objects.filter(league=league_id))

    kolejka_list = []

    if len(kolejki) > 0:
        kolejka_list = kolejka_list + kolejki

    if len(kolejki) == 0:

        if len(teams) % 2 != 0:
            t = Team.create("pauza")
            t.save()
            teams.append(t)

        number_of_kolejkas = len(teams) - 1
        half_size = len(teams) / 2
        teams_kolejkas = []
        teams_kolejkas = teams_kolejkas + teams
        teams_kolejkas.pop(0)
        team_size = len(teams_kolejkas)

        for k in range(0, number_of_kolejkas * 2):

            team_idx = k % team_size
            kolejka = Kolejka.create((k+1).__str__(), league)
            kolejka.save()
            new_match = Match.create(teams_kolejkas.__getitem__(team_idx), teams.__getitem__(0), league)
            new_match.save()
            kolejka.match_set.add(new_match)

            for i in range(1, half_size):
                first_team = (k + i) % team_size
                second_team = (k + team_size - i) % team_size
                new_match = Match.create(teams_kolejkas.__getitem__(first_team), teams_kolejkas.__getitem__(second_team), league)
                new_match.save()
                kolejka.match_set.add(new_match)
            kolejka_list.append(kolejka)
    return render(request, 'competition/season_teams.html', {'teams': teams, 'league_name': league_name, 'league_id': league_id, 'kolejka_list': kolejka_list})


def match(request):
    matches = Match.objects.all()
    context = {'matches': matches}
    return render(request, 'competition/match.html', context)


def match_details(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    facts = MatchFacts.objects.filter(match=match_id)
    context = {'match': match, 'facts': facts}
    return render(request, 'competition/match_detail.html', context)


def match_add(request):
    if request.method == 'POST':
        match_form = MatchForm(data=request.POST)
        if match_form.is_valid():
            new_match = match_form.save(commit=False)
            new_match.save()
        return redirect('competition:match')
    else:
        match_form = MatchForm()
        return render(request, 'competition/match_add.html', {'match_form': match_form})


def match_update(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    match_form = MatchForm(request.POST or None, instance=match)
    if request.method == 'POST' and match_form.is_valid():
        match_form.save()
        return redirect('competition:match')
    return render(request, 'competition/match_add.html', {'match_form': match_form})


def match_delete(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    match.delete()
    return redirect('competition:match')


def fact_add(request, match_id):
    if request.method == 'POST':
        fact_form = MatchFactForm(data=request.POST)
        if fact_form.is_valid():
            new_fact = fact_form.save(commit=False)
            new_fact.save()
        return redirect('competition:match_details', match_id=match_id)
    else:
        fact_form = MatchFactForm(initial={'match': match_id})
        return render(request, 'competition/fact_add.html', {'fact_form': fact_form})


def fact_delete(request, match_id, fact_id):
    fact = get_object_or_404(MatchFacts, pk=fact_id)
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


def league_table(request, league_id):
    table = []
    return render(request, 'competition/league_table.html', {'table': table})
