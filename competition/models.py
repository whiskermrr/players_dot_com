from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class LeagueType(models.Model):
    name1 = models.CharField(max_length=100)

    def __str__(self):
        return self.name1


class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Match(models.Model):
    host = models.ForeignKey(Team, related_name='matches_as_host', on_delete=models.CASCADE)
    guest = models.ForeignKey(Team, related_name='MatchGuest', on_delete=models.CASCADE)
    date = models.DateField(auto_created=False, auto_now=False)  # brak automatycznej daty przy stworzeniu i edycji
    hostGoals = models.PositiveIntegerField(validators=[MinValueValidator(0)])  # gole nie moga byc na minus
    guestGoals = models.PositiveIntegerField(validators=[MinValueValidator(0)]) # gole nie moga byc na minus

    def __str__(self):
        return "{}-{}-{}-{}-{}".format(self.host, self.guest, self.date, self.hostGoals, self.guestGoals)


class Kolejka(models.Model):
    name = models.ForeignKey(LeagueType, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.name, self.match)


class Table(models.Model):
    name = models.ForeignKey(Team, on_delete=models.CASCADE)
    name1 = models.ForeignKey(LeagueType, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(validators=[MinValueValidator(0)]) # nie mozna miec ujemnych pkt

    def __str__(self):
        return "{}-{}-{}".format(self.name, self.name1, self.points)


class Player(models.Model):
    name = models.CharField(max_length=100)
    sname = models.CharField(max_length=100)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1)]) # minimalny wiek gracza
    team = models.ForeignKey(Team)

    def __str__(self):
        return "{}-{}-{}".format(self.name, self.sname, self.team)


class MatchFacts(models.Model):
    match = models.ForeignKey(Match)
    player = models.ForeignKey(Player)
    incident = models.CharField(max_length=300)
    minute = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)]) # mecz trwa max 120 min

    def __str__(self):
        return "{}-{}-{}-{}".format(self.match, self.player, self.incident, self.minute)
