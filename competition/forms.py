from .models import Player
from django import forms
from .models import Team


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('name', 'sname', 'age', 'team')


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)
