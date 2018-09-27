from datetime import date
from random import choices

from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import models as authModels


# Create your models here.
from viewflow.models import Process


class Person(models.Model):
    SEX = [
        ['male']*2,
        ['female']*2,
        ]
    """ personal information"""
    firstname = models.CharField(max_length=200,blank=True)
    lastname = models.CharField(max_length=200,blank=True)
    birthdate = models.DateField(default=date.today, null=True, blank=True)
    sex = models.CharField(max_length=5, choices=SEX, blank=True)

    """  contact information"""
    email = models.EmailField()
    zip = models.PositiveIntegerField(blank=True, null=True,)


class Organisation(models.Model):
    """ An organization is an abstract concept for people or parties
        who organize themselves for a specific purpose.  Teams, clubs
        and associations are the 3 different organization types in this model"""

    name = models.CharField(max_length=300)
    founded_on = models.DateField()
    disolved_on = models.DateField()  # TODO: proper english
    description = models.TextField()


class Team(models.Model):
    """A Team is an organization owned by a Club. it consists of a list
       of players which is antemporary assignment of a player to a team
    """


pass


class Club(models.Model):
    pass


class Association(models.Model):
    pass


"""A player is a role of aperson in context of the sport.
   it holds"""


class Player(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()


class Membership(models.Model):
    """ A membership connects an organization with another organozation
        or peraon. It is reported by, and  confirmed by a person
        it my have a from and until date. missing values asumen an infinite Membership period
    """
    valid_until = models.DateField()
    valid_from = models.DateField()
    reporter: User = models.ForeignKey(
        authModels.User,
        on_delete=models.CASCADE,
        related_name="reported_%(class)ss",
        related_query_name="%(class)s_reporter")

    class Meta:
        abstract = True

    def is_active(self) -> bool:
        return self.valid_from <= date.now() <= self.valid_until


class PlayerToTeamMembership(Membership):
    player = models.ForeignKey(Person, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta(Membership.Meta):
        db_table = 'PlayerToTeamMembership'


class TeamToClubTeamMembership(Membership):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    class Meta(Membership.Meta):
        db_table = 'TeamToClubTeamMembership'


class ClubToAssociationMembership(Membership):
    team = models.ForeignKey(Club, on_delete=models.CASCADE)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)

    class Meta(Membership.Meta):
        db_table = 'ClubToAssociationMembership'


class PersonToAssociationMembership(Membership):
    ASSOCIATION_ROLES = (
        ['President']*2,
        ['Vicepresident']*2,
        ['Treasurer']*2,
        ['secretary']*2,
        ['Member']*2,
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)
    role = models.CharField(max_length=300, choices=ASSOCIATION_ROLES)

    class Meta(Membership.Meta):
        db_table = 'PersonToAssociationMembership'


    """
    player claim management objects
    """


class Claim(models.Model):
    """A claim is the initial object that is created, when an admin wants to add a player to his clb
    """
    membership = models.ForeignKey(PlayerToTeamMembership, on_delete=models.CASCADE)


class Receipt(models.Model):
    """A receipt is created when a claim is still standing after the deadline is reached
    """


class PlayerToTeamMembershipClaimProcess(Process):

    player = models.ForeignKey(Person, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    claims = models.ManyToManyField(Claim)
    receipts = models.ManyToManyField(Receipt)
    due_date = models.DateField()
    payment_due_date = models.DateField()



