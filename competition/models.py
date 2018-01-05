from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


class Season(models.Model):
    season = models.CharField(max_length=100)

    def __str__(self):
        return self.season


class LeagueType(models.Model):
    name = models.CharField(max_length=20)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=20)
    league = models.ManyToManyField(LeagueType)
    avatar = models.ImageField(upload_to='media/avatars')

    @classmethod
    def create(cls, name):
        team = cls(name=name)
        return team

    def __str__(self):
        return self.name


class Kolejka(models.Model):
    name = models.CharField(max_length=2)
    league = models.ForeignKey(LeagueType, on_delete=models.CASCADE, blank=True, null=True)

    @classmethod
    def create(cls, name, league):
        kolejka = cls(name=name, league=league)
        return kolejka

    def __str__(self):
        return "{}-{}".format(self.name, self.league)


class Match(models.Model):
    host = models.ForeignKey(Team, related_name='matches_as_host', on_delete=models.CASCADE)
    guest = models.ForeignKey(Team, related_name='MatchGuest', on_delete=models.CASCADE)
    kolejka = models.ForeignKey(Kolejka, on_delete=models.CASCADE, blank=True, null=True)
    league = models.ForeignKey(LeagueType, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now().strftime("%Y-%m-%d"), blank=True, null=True)  # data moze byc null
    hostGoals = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)  # gole nie moga byc na minus, moze byc null
    guestGoals = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True) # gole nie moga byc na minus, moze byc null

    @classmethod
    def create(cls, host, guest, league):
        match = cls(host=host, guest=guest, league=league)

        return match

    def __str__(self):
        return "{} {} : {} {}  {}".format(self.host, self.hostGoals, self.guestGoals, self.guest, self.date)


class Table(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    league = models.ForeignKey(LeagueType, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(validators=[MinValueValidator(0)], default=0) # nie mozna miec ujemnych pkt

    @classmethod
    def create(cls, team, league, points):
        table = cls(team=team, league=league, points=points)
        return table

    def __str__(self):
        return "{}-{}-{}".format(self.team, self.league, self.points)


class Player(models.Model):
    name = models.CharField(max_length=100)
    sname = models.CharField(max_length=100)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1)]) # minimalny wiek gracza
    team = models.ForeignKey(Team) # TODO not req

    def __str__(self):
        return "{}-{}-{}-{}".format(self.name, self.sname, self.age, self.team)


class MatchFacts(models.Model):
    INCIDENT_TYPE = (
        ('none', 'brak'),
        ('goal', 'gol'),
        ('sub in', 'zmiania wchodzi'),
        ('sub out', 'zmiana zchodzi'),
        ('yelow card', 'zolta kartka'),
        ('red card', 'czerwona kartka'),
    )
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    incident = models.CharField(max_length=15,
                                choices=INCIDENT_TYPE,
                                default='none')
    minute = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)]) # mecz trwa max 120 min

    def __str__(self):
        return "{}-{}-{}-{}".format(self.match, self.player, self.incident, self.minute)


class TeamStats(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    league = models.ForeignKey(LeagueType, on_delete=models.CASCADE)
    goalsScored = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    goalsLost = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    matchesWon = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    matchesLost = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    matchesDraw = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    scores = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    @classmethod
    def create(cls, team, league):
        teamStats = cls(team=team, league=league)
        return teamStats


    def addPoints(self, points, update):
        if update:
            self.scores += points
            value = 1
        else:
            self.scores -= points
            value = -1

        if points == 3:
            self.matchesWon += value
        elif points == 1:
            self.matchesDraw += value
        else:
            self.matchesLost += value


    def addScoredGoals(self, goals, update):
        if update:
            self.goalsScored += goals
        else:
            self.goalsScored -= goals

    def addLostGoals(self, goals, update):
        if update:
            self.goalsLost += goals
        else:
            self.goalsLost -=goals

    def __str__(self):
        return "{} {}".format(self.team, self.league)