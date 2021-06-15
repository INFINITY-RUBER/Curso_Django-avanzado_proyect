"""Users views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from cride.users.permissions import IsAccountOwner

# Serializers
from cride.users.serializers.profiles import ProfileModelSerializer
from cride.circles.serializers import CircleModelSerializer
from cride.users.serializers import (AccountVerificationSerializer,
                                     UserLoginSerializer, UserModelSerializer,
                                     UserSignUpSerializer)

# Models
from cride.users.models import User
from cride.circles.models import Circle


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """User view set.
    Manejar el registro, el inicio de sesión y la verificación de la cuenta.
    """

    queryset = User.objects.filter(
        is_active=True,
        is_client=True)  # filtra aquellos queestan activos y clientes
    serializer_class = UserModelSerializer
    lookup_field = 'username'  # en la url ira el nombre de usuario

    def get_permissions(self):
        """Asignar permisos según la acción."""
        if self.action in ['signup', 'login', 'verify']:
            permissions = [
                AllowAny
            ]  # si estan estas 3 acciones cualquiera puede entrar
        elif self.action in [
                'retrieve', 'update', 'partial_update', 'profile'
        ]:
            permissions = [
                IsAuthenticated, IsAccountOwner
            ]  # si esta en estas peticiones requiere estos permisos
        else:
            permissions = [IsAuthenticated]  # requieres una seccion si o si
        return [p() for p in permissions
                ]  # retornamos una instacia de "p" por cada permissions

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Iniciar sesión de usuario."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {'user': UserModelSerializer(user).data, 'access_token': token}
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """Registro de usuario."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Verificación de la cuenta."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulation, now go share some rides!'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, *args, **kwargs):
        """Actualizar los datos del perfil."""
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(profile,
                                            data=request.data,
                                            partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        """Agregue datos adicionales a la respuesta."""
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        circles = Circle.objects.filter(members=request.user,
                                        membership__is_active=True)
        #los circulos que pertenece este usuario
        data = {
            'user': response.data,
            'circles': CircleModelSerializer(circles, many=True).data
        }
        response.data = data
        return response


# class UserLoginAPIView(APIView):
#     """Users Login API views """
#     def post(self, request, *args, **kwargs):
#         """Handle HTTP POST request"""
#         serializer = UserLoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user, token = serializer.save()
#         data = {'user': UserModelSerializer(user).data, 'acces_token': token}
#         return Response(data, status=status.HTTP_201_CREATED)

# class UserSignUpAPIView(APIView):
#     """Users SignUp API views  """
#     def post(self, request, *args, **kwargs):
#         """Handle HTTP POST request"""
#         serializer = UserSignUpSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         data = UserModelSerializer(
#             user).data  # queremos regresar los mismos datos del usuario
#         return Response(data, status=status.HTTP_201_CREATED)

# class AccountVerificationAPIView(APIView):
#     """Account Verification API View  """
#     def post(self, request, *args, **kwargs):
#         """Handle HTTP POST request"""
#         serializer = AccountVerificationSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         data = {'message': 'Congratulations, now go share some rides!'}
#         return Response(data, status=status.HTTP_200_OK)