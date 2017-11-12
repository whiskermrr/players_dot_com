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

    # TEAM URLS
    # /competition/team
    url(r'^team/$', views.team, name='team'),
    # /competition/team/add
    url(r'^team/add/$', views.team_add, name='team-add'),
    # /competition/team/delete/8/
    url(r'^team/(?P<team_id>[0-9]+)/delete/$', views.team_delete, name='team_delete'),
    # /competition/team/update/8/
    url(r'^team/(?P<team_id>[0-9]+)/update/$', views.team_update, name='team_update'),

]
