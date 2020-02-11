from django.urls import path, include
from . import views
urlpatterns = [
    path('event/hook/', views.event_hook, name='event_hook'),
]