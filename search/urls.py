from django.urls import path
from . import views

urlpatterns = [
    path('', views.Search.as_view()),
    path('wordSearch', views.wordSearch),
    path('translateSentence', views.translateSentence),
]