from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.serializers import serialize
from .models import Tournament, Players, Database, Match, Team
from app.utils import stringifyImage
import json

#==========================================
#                   Utils
#==========================================
def JSONTournamentResponse(tournament, message):
    response = {
            "message" : message,
            "tournament": {
                "id": str(tournament.id),
                "name": tournament.tournament_name,
                "player_amount": tournament.player_amount,
                "completed": tournament.completed,
                "winner" : tournament.winner,
                "players": [{"name" : user.username} for user in tournament.players.all()],
                "matches": [{"id": match.id,
							"team1-id": match.team1.id,
                            "team1-score": match.team1.score,
                            "team1-players": [{"name": player.username} for player in match.team1.players.all()],
                            "team2-id": match.team2.id,
                            "team2-score": match.team2.score,
                            "team2-players": [{"name": player.username} for player in match.team2.players.all()],
							} for match in tournament.matches.all()],
            }
        }
    print (response)
    return (response)

def unknownMethod():
    return JsonResponse({'error': 'Method not supported'}, status=405)

#==========================================
#       Tournament Player Functions                                                                                                                                           
#==========================================
def tournamentAddPlayer(playerName, existing_tournament):

    player = Database.objects.filter(username=playerName).first()
    if player is None:
        return JsonResponse({'error': 'player not found'}, status=400)
    if existing_tournament.players.count() >= existing_tournament.player_amount:
        return JsonResponse({'error': 'too many players'}, status=400)
    existing_tournament.players.add(player)
    playerToReturn = {
        "username": player.username,
        "picture": stringifyImage(player.avatar_image) if player.avatar_image else None
    }
    return JsonResponse({'message': 'Player added successfully', 'player':  playerToReturn}, status=200)

def tournamentDeletePlayer(player, existing_tournament):
    if existing_tournament.players.filter(player.username).first() is None:
        return JsonResponse({'error': 'player does not exist within tournament'}, status=400)
    else:
        existing_tournament.players.remove(player)
        return JsonResponse({'succes!': 'player got removed'}, status=200)



#==========================================
#         Tournament Functions                                                                                                                                           
#==========================================
def createTurnament(request):
    data = json.loads(request.body)
    if "name" not in data or "number" not in data:
        return JsonResponse({'error': 'missing fields in request body'}, status=400)
    tournament = Tournament.objects.create(tournament_name=data['name'], player_amount=data['number'])
    tournament.players.add(request.user)
    return JsonResponse(JSONTournamentResponse(tournament, "Tournament created successfully"), status=200)

def getTournament(tournament):
    return JsonResponse(JSONTournamentResponse(tournament, "Tournament already exist"), status=200)


def deleteTournament(request, tournament):
    if tournament.completed == True:
        print("MOVE")
        request.user.completed_matches.add(tournament)
    else:
        print("DELE")
        for match in tournament.matches.all():
            match.delete()
        tournament.delete()
    return JsonResponse({'message': 'Succefully delete tournament'}, status=200)


#====================================================================================
#====================================================================================
#                               Tournament Manager
#====================================================================================
#====================================================================================
#==========================================
#         Tournament Management
#==========================================
def tournamentManager(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)
    existing_tournament = request.user.tournament
    if existing_tournament is not None:
        # Call the function from the switch dictionary
        match request.method:
            case "GET":
                return getTournament(existing_tournament)
            case "DELETE":
                return deleteTournament(request, existing_tournament)
            case "POST":
                deleteTournament(request, existing_tournament)
                return createTurnament(request)
            case _:
                return unknownMethod()
    else:
        if request.method == "POST":
            return createTurnament(request)
        else:
            return JsonResponse({'error': 'User does not have an tournament going'}, status=404)
        

#==========================================
#         TournamentID Manager
#==========================================
def tournamentManagerID(request, id=None):
    existing_tournament = Tournament.objects.filter(id=id).first()
    if existing_tournament is not None:
        # Call the function from the switch dictionary
        match request.method:
            case "GET":
                return getTournament(existing_tournament)
            case "DELETE":
                return deleteTournament(request, existing_tournament)
            case _:
                return unknownMethod()
    else:
        return JsonResponse({'error': 'User does not have an tournament going'}, status=404)

#==========================================
#         Tournament ID Player Management
#==========================================
def tournamentPlayerManager(request, id=None):
    existing_tournament = Tournament.objects.filter(id=id).first()
    data = json.loads(request.body)
    if "player" in data and existing_tournament is not None:
        match request.method:
            case "POST":
                return tournamentAddPlayer(data['player'], existing_tournament)
            case "DELETE":
                return tournamentDeletePlayer(data['player'], existing_tournament)
            case _:
                return unknownMethod()
    else:
        return JsonResponse({'error': 'something went wrong'}, status=400)


def tournamentAddMatch(request, existing_tournament):
    data = json.loads(request.body)
    if 'score1' not in data or 'player1' not in data or 'score2' not in data or 'player2' not in data:
        return JsonResponse({'error': 'missing felds in body'}, status=400)

    #Team one
    team1 = Team.objects.create()
    team1.score = data['score1']
    team1.players.add(data['player1'])
    if 'player2' in data:
        team1.players.add(data['player2'])

    #Team two
    team2 = Team.objects.create()
    team2.score = data['score2']
    team2.players.add(data['player3'])
    if 'player4' in data:
        team2.players.add(data['player4'])
    
    match = Match.objects.create(team1, team2)
    existing_tournament.matches.add(match)

#==========================================
#         Tournament ID Match Management
#==========================================
def tournamentMatchManager(request, id=None):
    existing_tournament = Tournament.objects.filter(id=id).first()
    if existing_tournament is not None:
        match request.method:
            case "POST":
                return tournamentAddMatch(request, existing_tournament)
            case _:
                return unknownMethod()
    else:
        return JsonResponse({'error': 'something went wrong'}, status=400)
