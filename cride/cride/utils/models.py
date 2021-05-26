"""Django models utilities """

# Django
from django.db import models


class CRideModel(models.Model):
    """Comparte Ride base model.
    CRideModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created (DateTime): Store the datetime the object was created.
        + modified (DateTime): Store the last datetime the object was modified.
    """
    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='date time on which the object was created.')
    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='date time on which the object was last modified.')

    class Meta:
        """Meta options."""

        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']


### EJEMPLOS DE HERENCIA PROXI MODEL ####

# class Person(models.Model):
#     first_name = models.Charfield()
#     last_name = models.Charfield()

# class MyPerson(Person):
#     class Meta:
#         proxy = True

#     def say_hi(name):
#         pass

# MyPerson.objects.all()
# ricardo = MyPerson.objects.get(pk=1)
# ricardo.say_hi('pablo')

# rulo = Person.objects.get(pk=2)
# rulo.say_hi('pablo')

# class Student(CRideModel):
#     name = models.Charfield()

#     class Meta(CRideModel.META):
#         db_table = 'student_role'
