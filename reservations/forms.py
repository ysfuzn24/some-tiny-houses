from django import forms
from .models import Reservation
from hotel.models import Room
from django.utils import timezone



class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room','check_in', 'check_out', 'guests', 'special_requests']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Kullanıcıyı formdan alıyoruz
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class ReservationSearchForm(forms.Form):
    check_in = forms.DateField(widget=forms.SelectDateWidget())
    check_out = forms.DateField(widget=forms.SelectDateWidget())
    guests = forms.IntegerField(min_value=1)

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        # Giriş tarihi çıkış tarihinden sonra olamaz
        if check_in and check_out and check_in >= check_out:
            raise forms.ValidationError('Giriş tarihi çıkış tarihinden önce olmalıdır.')

        # Giriş tarihinin geçmişte olmaması gerektiğini kontrol et
        if check_in and check_in < timezone.now().date():
            raise forms.ValidationError('Giriş tarihi geçmiş olamaz.')

        return cleaned_data
