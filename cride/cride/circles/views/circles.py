""" Circles views."""

# Django REST Framework
from rest_framework import viewsets, mixins

# permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.circles import IsCircleAdmin

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Serializers
from cride.circles.serializers import CircleModelSerializer

# Models
from cride.circles.models import Circle, Membership


class CircleviewsSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin, mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """ Circles views set."""

    serializer_class = CircleModelSerializer
    lookup_field = 'slug_name'  # lo busca por el nombre corto

    # Filters
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('slug_name', 'name')
    ordering_fields = ('rides_offered', 'rides_taken', 'name', 'created',
                       'member_limit')
    ordering = ('-member__count', '-rides_offered', '-rides_taken')
    # DjangoFilterBackend:
    filter_fields = ('verified', 'is_limited')

    def get_queryset(self):
        """Restringir la lista a solo público"""
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset

    def get_permissions(self):
        """Asignar permisos según la acción."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        """Administrador de círculos Assigh  """
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(user=user,
                                  profile=profile,
                                  circle=circle,
                                  is_admin=True,
                                  remaining_invitations=10)
