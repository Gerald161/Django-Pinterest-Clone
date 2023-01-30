from django.urls import path
from . import views

urlpatterns = [
    path('', views.Search.as_view()),
    path('<slug:slug>', views.wordSearch),
]