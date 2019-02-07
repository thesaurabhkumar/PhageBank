import django

django.setup()

from django.test.client import Client
from django.contrib.auth.models import User
from aloe import before, step, world, after

from faker import Faker

fake = Faker()

# world.us=fake.word()

# valid_credentials = {
#    'username': us,
#    'password': 'pass@123'}

browser = Client()


@before.all
def set_browser():
    world.browser = Client()


@step(r'When I fill in username with username, password with ([^\s]+) and email with ([^\s]+)')
def create_user(self, pwd, em):
    self.us = fake.word()
    print(self.us)
    user = User.objects.create(username=self.us, password=pwd, email=em)
    world.us = self.us
    user.save()


@step(r'Then the user should be saved in the database.')
def test_user_exist(self):
    # Check that login is successful with valid user
    response = world.browser.post('/login/', {'username': world.us, 'password': 'pass@123'}, follow=True)
    assert response.status_code == 200


@step(r'When I login with username ([^\s]+) and password ([^\s]+)')
def test_user_doesnt_exist(self, iv_user, iv_pwd):
    # Check that login is unsuccessful with invalid user
    world.response = browser.post('/login/', {'username': iv_user, 'password': iv_pwd}, follow=True)


@step(r'Then I should get error "(.*)"')
def assert_not_exist(self, err):
    index = world.response.content.find(err.encode())
    assert index != -1





