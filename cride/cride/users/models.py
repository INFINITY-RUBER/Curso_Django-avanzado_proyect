""" user model """

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# utilities
from cride.utils.models import CRideModel


class User(CRideModel, AbstractUser):
    """ user model.
    Extend from django is astract user, change the username field to
    to email and some extra fields"""
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={'unique': 'A user with that email already exists.'})

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message=
        "Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )

    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=17,
                                    blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_client = models.BooleanField(
        'client status',
        default=True,
        help_text=(
            'Ayude a distinguir fácilmente a los usuarios y realizar consultas.'
            'Los clientes son el principal tipo de usuario.'))

    is_verified = models.BooleanField(
        'verified',
        default=True,
        help_text=
        'Se establece en verdadero cuando el usuario ha verificado su dirección de correo electrónico.'
    )

    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username