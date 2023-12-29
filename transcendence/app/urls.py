from django.urls import path, re_path
from . import views

urlpatterns = [
    path("404", views.status_404, name="404"),
    path("_404", views.status_404, name="404"),
    path("login", views.loginUser, name="login"),
    path("login42", views.login42User, name="login"), #path created for login using 42 credentials (based on normal login page)
    path("signup", views.signup, name="signup"),
    path("logout", views.logoutUser, name="logout"),
    path("settings", views.settings, name="settings"),
    path("pong", views.pong, name="pong"),
	path("pong/1v1", views.pongOnevsOne, name="pong1v1"),
    path("pong/tournament", views.pongTournament, name="pongTournament"),
    path("pong/tournament/<int:id>", views.pongTournamentLobby, name="pongTournamentLobby"),
    path("pong/tournament/<int:id>/start", views.pongTournamentStart, name="pongTournamentStart"),
    path("pong/remoteTournament", views.remoteTournament, name="remoteTournament"),
	path("pong/remoteTournament/<int:id>", views.remoteLobby, name="remoteLobby"),
    path("postLogin", views.loginUser, name="postLogin"),
    path("postSignup", views.signup, name="postSignup"),
	path("users/<str:name>", views.usersPage, name="friendsPage"),

	path("getDoc/registerPlayer", views.getRegisterPlayersTemplate, name="registerPlayerTemplate"),
	path("getDoc/circleChart", views.getCircleChartTemplate, name="circleChartTemplate"),
	path("getDoc/searchItem", views.getSearchItem, name="searchItem"),
    path("getDoc/invitationItemTemplate", views.invitationItemTemplate, name="invitationItemTemplate"),
	path("getDoc/invitedItemTemplate", views.invitedItemTemplate, name="invitedItemTemplate"),
	path("getDoc/youAreInvitedItem", views.youAreInvitedItemTemplate, name="youAreInvitedItemTemplate"),
    path("getDoc/bracket4", views.bracketFourTemplate, name="bracket4Template"),
    path("getDoc/bracket8", views.bracketEightTemplate, name="bracket8Template"),
    path("getDoc/bracket16", views.bracketSixteenTemplate, name="bracket16Template"),
    re_path(r'^.*$', views.index, name='catch_all'),
    path("", views.index, name="index"),
]
