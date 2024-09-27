from django.urls import path
from .views import room_list, index, signup, contact_view, about_us


urlpatterns = [
    path('', index, name='index'),
    path('rooms/', room_list, name='room_list'),
    path('signup/',signup, name='signup'),
    path('contact/', contact_view, name='contact'), # rezervasyon sayfasından gidildiğinde hata düzeltilecek
    path('about_us/', about_us, name='about_us')
]