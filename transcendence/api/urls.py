from django.urls import path

from . import views

urlpatterns = [
    path("user", views.profilePicture, name="user"),
    path("tournament", views.tournament, name="tournament"),
	path("tournament/<int:id>", views.tournamentWithID, name="tournament"),
    path("tournament/player", views.tournamentPlayer, name="tournament/player"),
	path("tournament/player/<int:id>", views.tournamentPlayer, name="tournament/player"),
    path("oauth2/authorize", views.authorize, name="authorize"),
    path("oauth2/callback", views.callback, name="callback"),
]
