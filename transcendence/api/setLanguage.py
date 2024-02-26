from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def	setLanguage(request):
    if request.method != "POST":
        return redirect('/404')
    if not request.headers.get('flag'):
        return redirect('/404')
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": "false", "message": "redirect to 404"}, status=404)
    try:
        language = data['language']
    except KeyError:
        return redirect('/404')
    match language:
        case "eng":
            request.session['lang'] = "eng"
        case "fin":
            request.session['lang'] = "fin"
        case "swe":
            request.session['lang'] = "swe"
        case _:
            request.session['lang'] = "eng"
    return JsonResponse({"success": "true", "message": "success"}, status=200)
