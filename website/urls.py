from django.urls import path, include
from . import views
from .views import cemantix_game, hangman_game

urlpatterns = [
    path('', views.games_page, name='games_page'),
    path('cemantix', cemantix_game, name='cemantix_game'),
    path('hangman', hangman_game, name='hangman_game'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
]
