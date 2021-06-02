""" Circles URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import circles as circle_views
from .views import memberships as membership_views

router = DefaultRouter()
router.register(
    r'circles', circle_views.CircleviewsSet,
    basename='circle')  # me genera el Usa asi: www.**/circles/{id}/
router.register(r'circles/(?P<slug_name>[-a-zA-A0-0_]+)/members',
                membership_views.MembershipViewSet,
                basename='membership')

urlpatterns = [path('', include(router.urls))]
