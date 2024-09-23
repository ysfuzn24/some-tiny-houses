from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, ContactInfo, Reservation
from .forms import SignUpForm, ReservationForm
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
@login_required(login_url='/login/')
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

def reservation_view(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    print(room)

    if request.method == 'POST':
        print("request.POST:",request.POST)
        form = ReservationForm(request.POST)

        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']

            if room.is_available(check_in, check_out) > 0:
                reservation = form.save(commit=False)
                reservation.user = request.user
                reservation.room = room
                reservation.save()

                # Debug bilgilerinin yazdırılması
                print(settings.EMAIL_HOST_USER)
                print(reservation.user)
                print(reservation.user.email)

                # E-posta gönderimi
                send_mail(
                    'Rezervasyon Başarılı!',
                    f'Değerli {reservation.user.username},\n\nRezervasyonunuz başarıyla alınmıştır. Sizi {reservation.check_in} - {reservation.check_out} tarihleri arasında otelimizde ağırlamaktan büyük keyif duyacağız!\n\nSaygılarımızla,\nSome Tiny Houses Ekibi',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[reservation.user.email],
                    fail_silently=False,
                )

                return redirect('reservation_success')

            else:
                form.add_error(None, "Bu tarihler için oda müsait değil.")
    else:
        form = ReservationForm()

    return render(request, 'hotel/reservation.html', {'form': form, 'room': room})

def reservation_success_view(request):
    return render(request, 'hotel/reservation_success.html')

# İletişim bilgileri

def contact_view(request):
    contact_info = ContactInfo.objects.first()  # İlk iletişim bilgilerini al
    return render(request, 'hotel/contact.html', {'contact_info': contact_info})
