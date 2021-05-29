""" Circles URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import circles as circle_views

router = DefaultRouter()
router.register(
    r'circles', circle_views.CircleviewsSet,
    basename='circle')  # me genera el Usa asi: www.**/circles/{id}/

urlpatterns = [path('', include(router.urls))]
