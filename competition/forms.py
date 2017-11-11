from .models import Player
from django import forms


class PlayerForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = ('name', 'sname', 'age', 'team')