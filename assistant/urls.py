from django.urls import path
from .views import home, ask_ai

urlpatterns = [
    path("", home),
    path("ask/", ask_ai),
]
