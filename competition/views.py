from .models import LeagueType, Team, Match, Kolejka, Table, Player, MatchFacts
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from .forms import PlayerForm
from django.template.response import TemplateResponse
from .forms import TeamForm


def index(request):
    all_league = LeagueType.objects.all()
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


def team_delete(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team.delete()
    return redirect('competition:team')


def team_add(request):
    if request.method == 'POST':
        team_form = TeamForm(data=request.POST)
        if team_form.is_valid():
            new_team = team_form.save(commit=False)
            new_team.save()
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
