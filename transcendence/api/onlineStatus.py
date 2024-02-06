from django.http import JsonResponse
from django.shortcuts import redirect

def handleOnlineStatus(request):
    header = request.headers.get('triggerWindow')
    if header == None:
        return redirect('/404')
    if header == False:
        return redirect('/404')
    request.user.online_status = False
    request.user.full_clean()
    request.user.save()
    return JsonResponse({"success": "true", "message": "called successfuly"}, status=200)