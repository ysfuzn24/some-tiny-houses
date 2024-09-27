from django.shortcuts import render, redirect
from .models import Room, ContactInfo
from .forms import SignUpForm
from django.contrib.auth import login


def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'hotel/rooms.html', {'rooms': rooms})

def index(request):
    return render(request, 'hotel/index.html')

def about_us(request):
    return render(request, 'hotel/about_us.html')

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


# İletişim bilgileri

def contact_view(request):
    contact_info = ContactInfo.objects.first()  # İlk iletişim bilgilerini al
    return render(request, 'hotel/contact.html', {'contact_info': contact_info})
