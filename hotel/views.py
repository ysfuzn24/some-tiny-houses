from django.shortcuts import render,redirect
from .models import Room
from .forms import SignUpForm
from django.contrib.auth import login

# Create your views here.

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'hotel/room_list.html', {'rooms': rooms })

def index(request):
    return render(request, 'hotel/index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
