from .models import LeagueType, Team, Match, Kolejka, Table, Player, MatchFacts
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
# from .forms import UserForm
from django.template.response import TemplateResponse


def index(request):
    all_league = LeagueType.objects.all()
    context = {'all_league': all_league}
    return render(request, 'competition/index.html', context)


def player(request):
    all_players = Player.objects.all()
    context = {'all_players': all_players}
    return render(request, "competition/player.html", context)


def player_details(request, player_id):
    player = get_object_or_404(pk=player_id)
    return render(request, "competition/player_detail.html", {'player': player})


def team(request):
    all_teams = Team.objects.all()
    context = {'all_teams': all_teams}
    return render(request, "competition/team.html", context)
