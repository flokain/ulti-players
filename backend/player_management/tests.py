from datetime import date

from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from django.test import TestCase
from viewflow.models import Process
from .models import Person,Player


class Test(TestCase):

    def setUp(self):
        User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client.login(username='admin', password='password')
        self.person = Person.objects.create(email='test@test.com')
        self.player = self.person.player_set.create(number=97)

    def testApproved(self):
        response = self.client.post(
            '/player_management/process/start/',
            {'due_date': '2000-01-01',
             'payment_due_date': '2000-01-01',
             'player': self.player.pk,
             'team': self.player.pk,
             '_viewflow_activation-started': '2000-01-01'}
        )
        test = 0