"""Users views """

# Django REST framework
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView

# serializers
from cride.users.serializers import (UserLoginSerializer, UserModelSerializer,
                                     UserSignUpSerializer,
                                     AccountVerificationSerializer)


class UserLoginAPIView(APIView):
    """Users Login API views """
    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {'user': UserModelSerializer(user).data, 'acces_token': token}
        return Response(data, status=status.HTTP_201_CREATED)


class UserSignUpAPIView(APIView):
    """Users SignUp API views  """
    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request"""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(
            user).data  # queremos regresar los mismos datos del usuario
        return Response(data, status=status.HTTP_201_CREATED)


class AccountVerificationAPIView(APIView):
    """Account Verification API View  """
    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request"""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulations, now go share some rides!'}
        return Response(data, status=status.HTTP_200_OK)