from django.urls import path
from setuptools.extern import names

from someotelwebsite.settings import BASE_DIR
from . import views
from .views import room_list, index, signup, contact_view, about_us

urlpatterns = [
    path('', index, name='index'),
    path('rooms/', room_list, name='room_list'),
    path('signup/',signup, name='signup'),
    path('reservation/<int:room_id>/', views.reservation_view, name='reservation'),
    path('reservation/success/', views.reservation_success_view, name='reservation_success'),
    path('contact/', contact_view, name='contact'), # rezervasyon sayfasından gidildiğinde hata düzeltilecek
    path('about_us/', about_us, name='about_us')
]