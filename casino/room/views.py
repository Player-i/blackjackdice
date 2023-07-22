from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Room, Message

try:
    from django.utils import simplejson as json
except ImportError:
    import json
# Create your views here.

def rooms(request):
    context = {}
    rooms = Room.objects.all()
    context['rooms'] = rooms

    return render(request, 'templates/rooms.html', context) 

def create(request):
    print(" JOINING CREATE ")
    context = {}
    rooms = Room.objects.all()
    context['rooms'] = rooms
    if request.method == "GET":
        print(" LOADING CREATE ")
        return render(request, "templates/create.html", context)



def finish_bet(request):
    if request.method == "POST":
        user = request.user
        win_number = request.POST.get("win_number")
        win_number = int(win_number)
        print(win_number)
        context = {}
        context['win_number'] = win_number

        return HttpResponse(json.dumps(context), content_type="application/json")

def room(request, slug):
    context = {}
    room = Room.objects.get(slug=slug)
    if room.players < 2:
        room.players = room.players + 1
        room.players_username[request.user.username] = request.user.username
        room.save()
    messages = Message.objects.filter(room=room)[0:25]
    context['room'] = room
    context['messages'] = messages

    return render(request, 'templates/room.html', context)



