from django.contrib import admin
from .models import *


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'sname', 'age', 'team')


class MatchAdmin(admin.ModelAdmin):
    list_display = ('host', 'guest', 'date', 'hostGoals', 'guestGoals')


class KolejkaAdmin(admin.ModelAdmin):
    list_display = ('name', 'match')


class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'name1', 'points')


class MatchFactsAdmin(admin.ModelAdmin):
    list_display = ('match', 'player', 'incident', 'minute')



admin.site.register(Player, PlayerAdmin)
admin.site.register(LeagueType)
admin.site.register(Match, MatchAdmin)
admin.site.register(Kolejka, KolejkaAdmin)
admin.site.register(Team)
admin.site.register(Table, TableAdmin)
admin.site.register(MatchFacts, MatchFactsAdmin)
