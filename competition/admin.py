from django.contrib import admin
from .models import *


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('season',)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'sname', 'age', 'team')


class MatchAdmin(admin.ModelAdmin):
    list_display = ('host', 'guest', 'date', 'hostGoals', 'guestGoals')


class KolejkaAdmin(admin.ModelAdmin):
    list_display = ('name', 'league')


class TableAdmin(admin.ModelAdmin):
    list_display = ('team', 'league', 'points')


class MatchFactsAdmin(admin.ModelAdmin):
    list_display = ('match', 'player', 'incident', 'minute')


admin.site.register(Player, PlayerAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(LeagueType)
admin.site.register(Match, MatchAdmin)
admin.site.register(Kolejka, KolejkaAdmin)
admin.site.register(Team)
admin.site.register(Table, TableAdmin)
admin.site.register(MatchFacts, MatchFactsAdmin)
admin.site.register(TeamStats)
admin.site.register(PlayerStats)
