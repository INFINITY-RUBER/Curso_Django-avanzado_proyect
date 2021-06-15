"""Profile serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from cride.users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""
    class Meta:  # clase que va a definir los actributos
        """Meta class."""

        model = Profile
        # campos que quiero mostrar
        fields = ('picture', 'biography', 'rides_taken', 'rides_offered',
                  'reputation')
        read_only_fields = ('rides_taken', 'rides_offered', 'reputation'
                            )  # solo lectura
