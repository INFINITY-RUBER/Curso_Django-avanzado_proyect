""" User app. """

# Django
from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    """ User app config """
    name = 'cride.users'  # nombre de nuestra app
    verbose_name = 'Users'  # llamado en plural
