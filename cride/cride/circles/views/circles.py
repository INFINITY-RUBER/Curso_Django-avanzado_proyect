""" Circles views."""

# Django REST Framework
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Serializers
from cride.circles.serializers import CircleModelSerializer

# Models
from cride.circles.models import Circle


class CircleviewsSet(viewsets.ModelViewSet):
    """ Circles views set."""
    serializer_class = CircleModelSerializer
    permissions_classes = (IsAuthenticated, )

    def get_queryset(self):
        """ Restrict list to public-only"""
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset
