from .models import Player
from django import forms
from .models import Team, LeagueType, Match, MatchFacts


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('name', 'sname', 'age', 'team')


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'league',)

class LeagueForm(forms.ModelForm):
    class Meta:
        model = LeagueType
        fields = ('name',)

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('host', 'guest', 'date', 'hostGoals', 'guestGoals',)

class MatchFactForm(forms.ModelForm):
    class Meta:
        model = MatchFacts
        fields = ('match', 'player', 'incident', 'minute')