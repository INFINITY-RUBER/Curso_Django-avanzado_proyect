""" Users URLs."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import users as user_views
# from cride.users.views import (UserLoginAPIView, UserSignUpAPIView,
#                                AccountVerificationAPIView)

# urlpatterns = [
#     path('users/login/', UserLoginAPIView.as_view(), name='login'),
#     path('users/signup/', UserSignUpAPIView.as_view(), name='signup'),
#     path('users/verify/', AccountVerificationAPIView.as_view(), name='verify'),
# ]

router = DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')
urlpatterns = [path('', include(router.urls))]