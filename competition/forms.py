from .models import Player, Season
from django import forms
from .models import Team, LeagueType, Match, MatchFacts


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('name', 'sname', 'age', 'team')
        labels = {
            'name': 'Imie',
            'sname': 'Nazwisko',
            'age': 'Wiek',
            'team': 'Druzyna'
        }


class TeamForm(forms.ModelForm):

    name = forms.CharField(max_length=100)
    league = forms.ModelMultipleChoiceField(queryset=LeagueType.objects.filter(season__season=2017), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Team

        fields = ('name', 'league')
        labels = {
            'name': 'Nazwa',
            'league': 'Liga',
        }


class LeagueForm(forms.ModelForm):
    class Meta:
        model = LeagueType
        fields = ('name', 'season')
        labels = {
            'name': 'Nazwa',
            'season': 'Sezon',
        }


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('league', 'host', 'guest', 'date', 'hostGoals', 'guestGoals', 'kolejka',)
        labels = {
            'league': 'League',
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
