"""Permisos de usuario """

# Django REST framework
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """Permitir el acceso solo a los objetos propiedad del usuario solicitante."""
    def has_object_permission(self, request, view, obj):
        """Verifique que obj y usuario sean iguales."""
        return request.user == obj
