from django.urls import path
from . import views

urlpatterns = [
    path('', views.Pins.as_view()),
    # path('', ),
]