from django.conf.urls import url
from . import views

app_name = 'competition'


urlpatterns = [
    #LEAGUE URLS
    #index /competition
    url(r'^$', views.index, name='index'),

    # PLAYERS URLS
    #players /competition/player
    url(r'^player/$', views.player, name='player'),
    # players /competition/player/8/
    url(r'^player/(?P<player_id>[0-9]+)/$', views.player_details, name='player_details'),
    # players /competition/player/delete/8/
    url(r'^player/(?P<player_id>[0-9]+)/delete/$', views.player_delete, name='player_delete'),
    # players /competition/player/update/8/
    url(r'^player/(?P<player_id>[0-9]+)/update/$', views.player_update, name='player_update'),
    # player /competition/player/add
    url(r'^player/add/$', views.player_add, name='player-add'),


    # LEAGUES URLS
    # competition/8
    url(r'^league/(?P<league_id>[0-9]+)/$', views.league_details, name='league_details'),
    #competition/league/add/
    url(r'^league/add/$', views.league_add, name='league-add'),
    #competition/league/8/update/
    url(r'^league/(?P<league_id>[0-9]+)/update/$', views.league_update, name='league_update'),
    #competition/league/8/delete/
    url(r'^league/(?P<league_id>[0-9]+)/delete/$', views.league_delete, name='league_delete'),
    #competition/league/8/seasons
    url(r'^league/(?P<league_name>.+)/seasons/$', views.league_seasons, name='league_seasons'),
    # competition/ekstraklasa/2/teams
    url(r'^league/(?P<league_name>.+)/(?P<league_id>[0-9]+)/$', views.season_teams, name='season_teams'),
    # url(r'^league/(?P<league_name>.+)/(?P<season_id>[0-9]+)/teams$', views.league_seasons, name='league_season_teams'),

    # TEAM URLS
    # /competition/team
    url(r'^team/$', views.team, name='team'),
    #competition/team/8
    url(r'^team/(?P<team_id>[0-9]+)/$', views.team_details, name='team_details'),
    # /competition/team/add
    url(r'^team/add/$', views.team_add, name='team-add'),
    # /competition/team/delete/8/
    url(r'^team/(?P<team_id>[0-9]+)/delete/$', views.team_delete, name='team_delete'),
    # /competition/team/update/8/
    url(r'^team/(?P<team_id>[0-9]+)/update/$', views.team_update, name='team_update'),

    # MATCH URLS
    url(r'^match/$', views.match, name='match'),
    url(r'^match/(?P<match_id>[0-9]+)/$', views.match_details, name='match_details'),
    url(r'^match/add/$', views.match_add, name='match-add'),
    url(r'^match/(?P<match_id>[0-9]+)/update/$', views.match_update, name='match_update'),
    url(r'^match/(?P<match_id>[0-9]+)/delete/$', views.match_delete, name='match_delete'),

    # MATCH FACTS URLS
    url(r'match/(?P<match_id>[0-9]+)/fact/add/$', views.fact_add, name='fact_add'),
    url(r'match/(?P<match_id>[0-9]+)/fact/(?P<fact_id>[0-9]+)/update/$', views.fact_update, name='fact_update'),
    url(r'match/(?P<match_id>[0-9]+)/fact/(?P<fact_id>[0-9]+)/delete/$', views.fact_delete, name='fact_delete'),

    #TABELA
    url(r'table/(?P<league_id>[0-9]+)/(?P<league_name>.+)/$', views.league_table, name='league_table'),

]