from django.urls import path, include
from . import views
from .views import cemantix_game

urlpatterns = [
    path('games/', views.games_page, name='games_page'),
    path('', cemantix_game, name='cemantix_game'),
]
