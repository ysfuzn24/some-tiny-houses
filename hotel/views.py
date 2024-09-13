from django.shortcuts import render
from .models import Room

# Create your views here.

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'hotel/room_list.html', {'rooms': rooms })

def index(request):
    return render(request, 'hotel/index.html')
