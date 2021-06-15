"""Circle serializers."""

# Django REST Framework
from rest_framework import serializers

#Models
from cride.circles.models import Circle


class CircleModelSerializer(serializers.ModelSerializer):
    """ Circles Model Serializer"""

    members_limit = serializers.IntegerField(required=True,
                                             min_value=10,
                                             max_value=32000)
    is_limited = serializers.BooleanField(default=False)

    class Meta:
        """Meta class."""
        model = Circle
        fields = ('name', 'slug_name', 'about', 'picture', 'rides_offered',
                  'rides_taken', 'verified', 'is_public', 'is_limited',
                  'members_limit')
        # campos solo lectura
        read_only_fields = ('is_public', 'verified', 'rides_offered',
                            'rides_taken')

    def validate(self, data):
        """ Asegúrese de que tanto members_limit como is_limited estén presentes."""
        members_limit = data.get('members_limit', None)
        is_limited = data.get('is_limited', False)
        if is_limited ^ bool(members_limit):  # operación XOR en los operandos
            raise serializers.ValidationError(
                'si el círculo es limitado, se debe proporcionar un límite de miembros'
            )
        return data
