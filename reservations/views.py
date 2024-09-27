from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm, ReservationSearchForm
from django.core.mail import send_mail
from django.conf import settings
from hotel.models import Room
from django.contrib.auth.decorators import login_required
from .models import Reservation


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Room
from .forms import ReservationForm

@login_required(login_url='/login/')
def reservation_view(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    # Giriş ve çıkış tarihlerini query parametrelerinden al
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    if request.method == 'POST':
        form = ReservationForm(request.POST, user=request.user)  # Kullanıcı bilgisini ekliyoruz

        if form.is_valid():
            # Formdan verileri al
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            room = form.cleaned_data['room']

            # Oda müsait mi kontrol et
            if room.is_available(check_in, check_out):
                reservation = form.save(commit=False)  # Önce kaydetmiyoruz
                reservation.user = request.user  # Kullanıcı bilgisini atıyoruz
                reservation.save()  # Şimdi kaydet

                # E-posta gönderimi
                try:
                    send_mail(
                        'Rezervasyon Başarılı!',
                        f'Değerli {reservation.user.username},\n\nRezervasyonunuz başarıyla alınmıştır. '
                        f'Sizi {reservation.check_in} - {reservation.check_out} tarihleri arasında otelimizde '
                        'ağırlamaktan büyük keyif duyacağız!\n\nSaygılarımızla,\nSome Tiny Houses Ekibi',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[reservation.user.email],
                        fail_silently=False,
                    )
                except Exception:
                    form.add_error(None, "Rezervasyon tamamlandı, ancak e-posta gönderilemedi. Lütfen iletişime geçin.")

                return redirect('reservation_success')
            else:
                form.add_error(None, "Maalesef, seçtiğiniz tarihlerde bu oda dolu. Lütfen başka tarihler deneyin.")

    else:
        # Eğer form POST değilse, check_in ve check_out değerleri ile formu doldur
        form = ReservationForm(initial={
            'check_in': check_in,
            'check_out': check_out,
            'room': room  # Odayı da başlangıç değerine ekliyoruz
        })

    return render(request, 'reservation.html', {
        'form': form,
        'room': room,
        'check_in': check_in,
        'check_out': check_out
    })


def reservation_success_view(request):
    return render(request, 'reservation_success.html')


@login_required(login_url='/login/')
def room_search_view(request):
    available_rooms = []
    form = ReservationSearchForm()

    if request.method == 'POST':
        form = ReservationSearchForm(request.POST)

        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            guests = form.cleaned_data['guests']

            # Uygun odaları bulma
            available_rooms = Room.objects.filter(
                max_occupancy__gte=guests
            ).exclude(
                reservations__check_in__lt=check_out,
                reservations__check_out__gt=check_in
            ).distinct()

    return render(request, 'room_search.html', {
        'form': form,
        'available_rooms': available_rooms,
        'check_in': request.POST.get('check_in'),
        'check_out': request.POST.get('check_out')
    })
