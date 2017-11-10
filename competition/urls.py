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
    url(r'^player/(?P<pk>[0-9]+)/$', views.player, name='player_details'),

    # TEAM URLS
    #team /competition/team
    url(r'^team/$', views.team, name='team'),
]
