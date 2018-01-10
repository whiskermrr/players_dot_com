from .models import Player, Season
from django import forms
from .models import Team, LeagueType, Match, MatchFacts


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'sname', 'age', 'team']
        labels = {
            'name': 'Imie',
            'sname': 'Nazwisko',
            'age': 'Wiek',
            'team': 'Druzyna'
        }


class TeamForm(forms.ModelForm):

    name = forms.CharField(max_length=100)
    league = forms.ModelMultipleChoiceField(queryset=LeagueType.objects.all(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Team

        fields = ['avatar', 'name', 'league']
        labels = {
            'avatar': 'Avatar',
            'name': 'Nazwa',
            'league': 'Liga',
        }


class LeagueForm(forms.ModelForm):
    class Meta:
        model = LeagueType
        fields = ['name']
        labels = {
            'name': 'Nazwa',
        }


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['season']
        labels  = {
            'season': 'Season',
        }


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['season', 'host', 'guest', 'date', 'hostGoals', 'guestGoals', 'kolejka',]
        labels = {
            'season': 'League',
            'host': 'Gospodarz',
            'guest': 'Gosc',
            'date': 'Data',
            'hostGoals': 'Gole gospodarze',
            'guestGoals': 'Gole goscie',
            'kolejka': 'kolejka'
        }


class MatchFactForm(forms.ModelForm):
    class Meta:
        model = MatchFacts
        fields = ('match', 'player', 'incident', 'minute')
        labels = {
            'match': 'Mecz',
            'player': 'Gracz',
            'incident': 'Zdarzenie',
            'minute': 'Minuta',
        }
