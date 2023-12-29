from django.urls import path

from . import views

urlpatterns = [
    path("user", views.profilePicture, name="user"),
    path("tournament", views.tournament, name="tournament"),
	path("tournament/<int:id>", views.tournamentWithID, name="tournament"),
    path("tournament/player", views.tournamentPlayer, name="tournament/player"),
	path("tournament/player/<int:id>", views.tournamentPlayer, name="tournament/player"),
    # Below you can see all the paths and views created to simulate the access to the 42API,
	#they need to be moved to APP(root) since we will not be using the api url path in order to login with 42
    path("oauth2/authorize", views.authorize, name="authorize"),
    path("oauth2/callback", views.callback, name="callback"),
    path("oauth2/fetch", views.fetchData, name="fetch"),
]
