"""Vistas de membresía del círculo."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from cride.circles.models import Circle, Membership, Invitation

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember, IsSelfMember  # permisos por miembros

# Serializers
from cride.circles.serializers import MembershipModelSerializer, AddMemberSerializer


class MembershipViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Conjunto de vistas de miembros del círculo."""

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs
                 ):  # con este metodo ara la verificacion del circulo primero
        """Verify that the circle exists."""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args,
                                                       **kwargs)

    def get_permissions(self):
        """Asignar permisos según la acción."""
        permissions = [IsAuthenticated,
                       IsActiveCircleMember]  # por defaul IsAuthenticated
        if self.action != 'create':
            permissions.append(IsActiveCircleMember)
        if self.action == 'invitations':
            permissions.append(IsSelfMember)
        return [p() for p in permissions]

    def get_queryset(self):
        """Regresar miembros del círculo."""
        return Membership.objects.filter(
            circle=self.circle,
            is_active=True  # solo los activas se mostraran
        )

    def get_object(self):
        """Devuelve el miembro del círculo usando el nombre de usuario del usuario."""
        return get_object_or_404(Membership,
                                 user__username=self.kwargs['pk'],
                                 circle=self.circle,
                                 is_active=True)

    def perform_destroy(self, instance):
        """Deshabilitar la membresía."""
        instance.is_active = False
        instance.save()

    @action(detail=True, methods=['get'])
    def invitations(self, request, *args, **kwargs):
        """Recuperar el desglose de las invitaciones de un miembro.

        Devolverá una lista que contiene todos los miembros
         que han utilizado sus invitaciones y otra lista que
         contiene las invitaciones que aún no se han utilizado.
        """
        member = self.get_object()
        invited_members = Membership.objects.filter(
            circle=self.circle, invited_by=request.user,
            is_active=True)  # query a quien invito

        unused_invitations = Invitation.objects.filter(
            circle=self.circle, issued_by=request.user,
            used=False).values_list('code')

        diff = member.remaining_invitations - len(unused_invitations)

        invitations = [x[0] for x in unused_invitations]

        for i in range(0, diff):
            invitations.append(
                Invitation.objects.create(issued_by=request.user,
                                          circle=self.circle).code)
        data = {
            'used_invitations':
            MembershipModelSerializer(invited_members, many=True).data,
            'invitations':
            invitations
        }
        return Response(data)

    def create(self, request, *args, **kwargs):
        """Handle member creation from invitation code."""
        serializer = AddMemberSerializer(data=request.data,
                                         context={
                                             'circle': self.circle,
                                             'request': request
                                         })
        serializer.is_valid(raise_exception=True)
        member = serializer.save()

        data = self.get_serializer(member).data
        return Response(data, status=status.HTTP_201_CREATED)