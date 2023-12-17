from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.serializers import serialize
from .models import Tournament, Players, CustomUserData
from app.forms import ProfilePicture
from app.views import loginUser
from django.shortcuts import render
import json


#==========================================
#          Profile Picture
#==========================================

def profilePicture(request):
    if not request.user.is_authenticated:
        return loginUser(request)
    if request.method == 'POST':
        form = ProfilePicture(request.POST, request.FILES)
        if form.is_valid():
            request.user.avatarImage = form.cleaned_data['avatarImage']
            request.user.save()
            url = request.user.avatarImage.url if request.user.avatarImage else None
            return JsonResponse({"avatar_url": url, "message": "Avatar image updated sucessfully"}, status=200)
        else:
            print("Invalid form");
            print(form.errors)
            return JsonResponse({"success": "false", "message": "Failed to update the avatar picture"}, status=400)
    else:
        if request.user.avatarImage == None:
            form = ProfilePicture()
        else:
            form = ProfilePicture(initial={
                'avatarImage' : request.user.avatarImage,
            })
    context = {
        "form": form,
        "content": "dashboard.html"
    }
    return render(request, 'index.html', context)

#==========================================
#       Tournament Player Management
#==========================================
def tournamentPlayer(request):
    data = json.loads(request.body)

    print ("paler")

    if(request.method == "POST"):
        print ("method POST")
        if "player" not in data or "id" not in data:
          return JsonResponse({'error': 'missing fields in request body'}, status=400)
        tournament = Tournament.objects.filter(id=data['id'])
        player = Players.objects.create(name=data['player'])
        if tournament.exists():
            tournament.first().players.add(player)
        else:
          return JsonResponse({'error': 'tournament does not exist'}, status=400)
        playerdict = model_to_dict(player)
        return JsonResponse({'message': 'Player added successfully', 'player': playerdict}, status=200)

    elif(request.method == "PUT"):
        print ("method PUT")
        print (data)
        if "id" not in data or "username" not in  data:
          return JsonResponse({'error': 'missing fields in request body'}, status=400)
        player = Players.objects.filter(id=data['id'])
        if player.exists():
            print ("AAAAAA")
            player_instance = player.first()
            player_instance.name =  data["username"]
            player_instance.save()
        else:
          return JsonResponse({'error': 'player does not exist'}, status=400)
        playerdict = model_to_dict(player.first())
        print (playerdict)
        return JsonResponse({'message': 'Player name change succefull', 'player': playerdict}, status=200)

    elif(request.method == "DELETE"):
        print ("method DELETE")
        print (data)

        if "playerID" not in data or "id" not in  data:
          return JsonResponse({'error': 'missing fields in request body'}, status=400)
        tournament = Tournament.objects.filter(id=data['id'])
        player = Players.objects.filter(id=data['playerID'])
        if player.exists() and tournament.exists():
            tournament.first().players.remove(player.first())
            player.first().delete()
        else:
          return JsonResponse({'error': 'player or tournament does not exist'}, status=400)

    else:
        return JsonResponse({'error': 'We dont handle this request here'}, status=400)


#==========================================
#           Tournament Management
#==========================================

def createTournamentResponse(tournament, message):
    response = {
            "message" : message,
            "tournament": {
                "id": str(tournament.id),
                "uuid": tournament.uuid,
                "name": tournament.name,
                "amount": tournament.amount,
                "state": tournament.sate,
                "players": [{"name" : player.name, "id" : player.id} for player in tournament.players.all()],
            }
        }
    return (response)

def tournament(request):
    #Validate request
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)

    existing_tournament = Tournament.objects.filter(uuid=request.user.uuid)

    if(request.method == "GET"):
        #if user already has i tournemnt on going return it.
        if existing_tournament.exists():
            return JsonResponse(createTournamentResponse(existing_tournament.first(), "Tournament already exist"), status=200)
        else:
            return JsonResponse({'error': 'User does not have an tournament going'}, status=404)

    elif(request.method == "POST"):

        #if user already has a tournemnt on going return it.
        if existing_tournament.exists():
            existing_tournament.first().delete()
            # return JsonResponse(createTournamentResponse(existing_tournament.first(), request.user.uuid, "Tournament already exist"), status=200)

        data = json.loads(request.body)
        if "name" not in data or "number" not in data:
            return JsonResponse({'error': 'missing fields in request body'}, status=400)

        #Create a tournament object and add the player to it
        tournament = Tournament.objects.create(name=data['name'], amount=data['number'], uuid=request.user.uuid)
        playerName = Players.objects.create(name=data['player'])
        tournament.players.add(playerName)
        return JsonResponse(createTournamentResponse(tournament, "Tournament created successfully"), status=200)

    elif(request.method == "DELETE"):

        if existing_tournament.exists():
            existing_tournament.first().delete()
            return JsonResponse({'message': 'Succefully delete tournament'}, status=200)
        else:
            return JsonResponse({'error': 'User does not have an tournament going'}, status=400)

    else:

        return JsonResponse({'error': 'We dont handle this request here'}, status=400)


#==========================================
#      Tournament Management With ID
#==========================================
def tournamentWithID(request, id):
    existing_tournament = Tournament.objects.filter(id=id)

    if(request.method == "GET"):
        if existing_tournament.exists():
            return JsonResponse(createTournamentResponse(existing_tournament.first(), "Tournament already exist"), status=200)
        else:
            return JsonResponse({'error': 'This tournament ID does not exist'}, status=400)
    elif(request.method == "DELETE"):
        if existing_tournament.exists():
            for player in existing_tournament.first().players.all():
                player.delete()
            existing_tournament.first().delete()
            return JsonResponse({'message': 'Succefully delete tournament'}, status=200)
        else:
            return JsonResponse({'error': 'This tournament ID does not exist'}, status=400)
    else:
        return JsonResponse({'error': 'We dont handle this request here'}, status=400)

    response = {
        "message" : "Tournament created successfully",
        "tournament": {
            "id": str(tournament.id),
            "name": tournament.name,
            "amount": tournament.amount,
            "state": tournament.sate,
            "players": [player.name for player in tournament.players.all()],
        }
    }
    # tournamentdict = model_to_dict(tournament)
    # tournamentdict['players'] = list(tournament.players.values_list('name', flat=True))

    return JsonResponse(response, status=200)
