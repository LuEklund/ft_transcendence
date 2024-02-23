from django.http import JsonResponse, QueryDict
from django.forms.models import model_to_dict
from .models import Database
from app.forms import ProfilePicture
from app.utils import stringifyImage, setOffline, setOnline, getTextsForLanguage
from django.shortcuts import redirect
from django.contrib.auth import logout
from .translations.translation import pages
import json

#==========================================================================
#                (REQUEST) ADD Friend and REMOVE Friend
#==========================================================================
def friendRequest(request, friendName=None):
    user = request.user
    if not user.is_authenticated:
        return redirect('/login')
    if user.is_login == False:
        setOffline(user=request.user)
        logout(request)
        return redirect('/login')
    setOnline(user=request.user)
    if (request.method == "GET" and friendName==None):
        requests = []
        for friend_request in user.friend_requests.all():
            FriendObject = {
                "username" : friend_request.username,
                "avatar_image" : stringifyImage(friend_request) if friend_request.avatar_image else None
            }
            requests.append(FriendObject)
        return JsonResponse(requests, status=200, safe=False)
    potentailFriend = Database.objects.filter(username=friendName).first()
    if potentailFriend is None:
        return JsonResponse({"message":getTextsForLanguage(pages["error"], request)["NonExistingUser"]}, status=400)
    if user == potentailFriend:
        return JsonResponse({"message":getTextsForLanguage(pages["error"], request)["FriendIsSelf"]}, status=400)
    match request.method:
        case "POST":
            if user.friends.filter(username=potentailFriend.username).exists():
                return JsonResponse({"message":getTextsForLanguage(pages["error"], request)["FriendsAlready"]}, status=400)
            if potentailFriend.friend_requests.filter(username=user.username).exists():
                return JsonResponse({"message":getTextsForLanguage(pages["error"], request)["FriendsRequestSentAlready"]}, status=400)
            if user.friend_requests.filter(username=potentailFriend.username).exists():
                user.friend_requests.remove(potentailFriend)
                user.friends.add(potentailFriend)
                return JsonResponse({"message":"Both sent friend request, firendship established!"}, status=200)
            else:
                potentailFriend.friend_requests.add(user)
                return JsonResponse({"message":"Success sent friend request"}, status=200)
        case "DELETE":
            if user.friend_requests.filter(username=potentailFriend.username).exists():
                user.friend_requests.remove(potentailFriend)
                user.full_clean()
                user.save()
                return JsonResponse({"message":"Success removed friend request"}, status=200)
            return JsonResponse({"message": getTextsForLanguage(pages["error"], request)["NoFriendRequestSent"]}, status=400)
        case _:
            return JsonResponse({"message": getTextsForLanguage(pages["error"], request)["MethodNotImplemented"]}, status=405)






#==========================================================================
#                   ACCEPT Friend and REMOVE Friend
#==========================================================================
def friends(request, friendName=None):
    user = request.user
    if not user.is_authenticated:
        return redirect('/login')
    if user.is_login == False:
        setOffline(user=request.user)
        logout(request)
        return redirect('/login')
    setOnline(user=request.user)
    friend = Database.objects.filter(username=friendName).first()
    if friend is None:
        return JsonResponse({"message":getTextsForLanguage(pages["error"], request)["NonExistingUser"]}, status=400)
    match request.method:
        case "POST":
            if user.friend_requests.filter(username=friend.username).exists():
                user.friend_requests.remove(friend)
                user.friends.add(friend)
                return JsonResponse({"message":"Success added friend"}, status=200)
            return JsonResponse({"message":getTextsForLanguage(pages["error"], request)["NoFriendRequest"]}, status=400)
        case "DELETE":
            if user.friends.filter(username=friend.username).exists():
                user.friends.remove(friend)
                return JsonResponse({"message":"Success removed friend"}, status=200)
            return JsonResponse({"message":getTextsForLanguage(pages["error"], request)["NotFriends"]}, status=400)
        case _:
            return JsonResponse({"message": getTextsForLanguage(pages["error"], request)["MethodNotImplemented"]}, status=405)



#==========================================================================
#         GET USER FRIENDS (Returns all friends of the logged in user)
#==========================================================================
def getFriends(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/login')
    if user.is_login == False:
        setOffline(user=request.user)
        logout(request)
        return redirect('/login')
    setOnline(user=request.user)
    if request.method != "GET":
        return JsonResponse({"message": getTextsForLanguage(pages["error"], request)["MethodNotImplemented"]}, status=405)
    user_friends = []
    for friend in user.friends.all():
        user_friend = {
            "username" : friend.username,
            "avatar_image" : stringifyImage(friend) if friend.avatar_image else None,
            "online_status" : friend.online_status,
        }
        user_friends.append(user_friend)
    return JsonResponse(user_friends, status=200, safe=False)


#==========================================================
#         USER SEARCH (Return all associated users)
#==========================================================
def searchUsers(request, search=None):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.user.is_login == False:
        setOffline(user=request.user)
        logout(request)
        return redirect('/login')
    setOnline(user=request.user)
    if request.method != "GET":
        return JsonResponse({"message": getTextsForLanguage(pages["error"], request)["MethodNotImplemented"]}, status=405)
    users = Database.objects.filter(username__icontains=search)
    user_friends = []
    for user in users:
        user_friend = {
            "username" : user.username,
            "avatar_image" : stringifyImage(user) if user.avatar_image else None,
        }
        user_friends.append(user_friend)
    return JsonResponse(user_friends, status=200, safe=False)

#==========================================================
#         GET SPECIFIC USER
#==========================================================

def getUserStats(user):
    userInfo = {
        "username" : user.username,
        "online_status" : user.online_status,
        "is_login" : user.is_login,
        "is_42" : user.is_42,
        "friends" : [{
            'username': friend.username,
            'avatar_image': stringifyImage(friend) if friend.avatar_image else None
        } for friend in user.friends.all()],
        "friend_requests" :[{
            'username': friend_request.username,
            'avatar_image': stringifyImage(friend_request) if friend_request.avatar_image else None
        } for friend_request in user.friend_requests.all()],
        "coallition" : user.coallition,
        "access_token" : user.access_token,
        "refresh_token" : user.refresh_token,
        "expiration_time" : user.expiration_time,
        "avatar_image" : stringifyImage(user) if user.avatar_image else None,
        "completed_matches" : [{
            "id" : match.id,
            "teamOne" : {
                "id" : match.team1.id,
                "winner" : match.team1.winner,
                "score" : match.team1.score,
                "players" : [{
                    "username" : player.username,
                    'avatar_image': stringifyImage(player) if player.avatar_image else None
                } for player in match.team1.players.all()],
            },
            "teamTwo" : {
                "id" : match.team2.id,
                "winner" : match.team2.winner,
                "score" : match.team2.score,
                "players" : [{
                    "username" : player.username,
                    'avatar_image': stringifyImage(player) if player.avatar_image else None
                } for player in match.team2.players.all()],
            },
            "date" : match.date,
        } for match in user.completed_matches.all()],
        "total_points_scored" : user.total_points_scored,
        "total_points_conceded" : user.total_points_conceded,
        "matches_played" : user.matches_played,
        "matches_won" : user.matches_won,
        "tournaments_played" : user.tournaments_played,
        "tournaments_won" : user.tournaments_won,
    }
    return(userInfo)


def getUser(request, userName=None):
#I removed the check for if the user is authenticated or not. Because, before calling getUser, we check it in usersPage function. The completed is not gonna change, because getUser is being called just there.
    user = Database.objects.filter(username=userName).first()
    if user is None:
        return JsonResponse({'error': getTextsForLanguage(pages["error"], request)["NonExistingUser"]}, status=400)
    if request.method == "GET":
        userInfo = getUserStats(user)
        return JsonResponse(userInfo, status=200, safe=False)
    return JsonResponse({"message": getTextsForLanguage(pages["error"], request)["MethodNotImplemented"]}, status=405)

#==========================================================
#         GET LOGGED IN USER
#==========================================================
def Users(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.user.is_login == False:
        setOffline(user=request.user)
        logout(request)
        return redirect('/login')
    setOnline(user=request.user)
    user = request.user
    match request.method:
        case "GET":
            userInfo = getUserStats(user)
            return JsonResponse(userInfo, status=200, safe=False)
        case "DELETE":
            user.delete()
            return JsonResponse({"message":"Success"}, status=200, safe=False)
        case _:
            return JsonResponse({"message": getTextsForLanguage(pages["error"], request)["MethodNotImplemented"]}, status=405)


#==========================================
#          Profile Picture
#==========================================

def profilePicture(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.user.is_login == False:
        setOffline(user=request.user)
        logout(request)
        return redirect('/login')
    setOnline(user=request.user)
    if request.method == 'POST':
        form = ProfilePicture(request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user)
            source = stringifyImage(request.user)
            return JsonResponse({"source": source, "message": "Avatar image updated sucessfully"}, status=200)
        else:
            return JsonResponse({"success": "false", "message": getTextsForLanguage(pages["error"], request)["FailedToUpdateAvatarImage"]}, status=400)
    return JsonResponse({"success": "false", "message": getTextsForLanguage(pages["error"], request)["MethodNotImplemented"]}, status=400)

