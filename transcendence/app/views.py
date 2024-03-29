from django.shortcuts import render, redirect
from . import errors
from . import mainPage
from . import userInterface
from . import pongTournament
from .utils import getTextsForLanguage
from api.translations.translation import pages

def getRegisterPlayersTemplate(request):
    if not request.user.is_authenticated:
        return redirect("/404")
    if not request.headers.get("flag"):
        return redirect("/404")
    return render(request, "registeredPlayers.html", {})

def getCircleChartTemplate(request):
    if not request.user.is_authenticated:
        return redirect("/404")
    if not request.headers.get("flag"):
        return redirect("/404")
    return render(request, "circleChart.html", {})

def getSearchItem(request):
    if not request.user.is_authenticated:
        return redirect("/404")
    if not request.headers.get("flag"):
        return redirect("/404")
    return render(request, "SearchElements/searchItem.html", {})
def invitedItemTemplate(request):
    if not request.user.is_authenticated:
        return redirect("/404")
    if not request.headers.get("flag"):
        return redirect("/404")
    return render(request, "PongTournamentPages/invitedItem.html", {})
def bracketFourTemplate(request):
    if not request.user.is_authenticated:
        return redirect("/404")
    if not request.headers.get("flag"):
        return redirect("/404")
    context = {
        "texts": getTextsForLanguage(pages["tournamentBoard"], request)
    }
    return render(request, "TournamentBrackets/tournamentBracket4.html", context)
def bracketEightTemplate(request):
    if not request.user.is_authenticated:
        return redirect("/404")
    if not request.headers.get("flag"):
        return redirect("/404")
    return render(request, "TournamentBrackets/tournamentBracket8.html", {})
def getFriendItem(request):
    if not request.user.is_authenticated:
        return redirect("/404")
    if not request.headers.get("flag"):
        return redirect("/404")
    return render(request, "SearchElements/friendItem.html", {})
def getInvitationItemTemplate(request):
    if not request.user.is_authenticated:
        return redirect("/404")
    if not request.headers.get("flag"):
        return redirect("/404")
    context = {
        "texts": getTextsForLanguage(pages["invitations"], request)
    }
    return render(request, "SearchElements/invitationItem.html", context)
