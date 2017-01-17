from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Event


class AuthForm (AuthenticationForm):
    username = forms.CharField(
        required=True,
        label='Имя пользователя',
        widget=forms.widgets.TextInput(
            attrs={'placeholder': 'Ваше имя'}
        )
    )



    password = forms.CharField(
        required=True,
        label='Пароль',
        widget=forms.widgets.PasswordInput(
            attrs={'placeholder': 'Пароль'}
        )
    )

    class Meta:
        fields = ['username', 'password']
        model = User


class RegistrationForm (UserCreationForm):
    username = forms.CharField(
        required=True,
        label='Имя пользователя',
        widget=forms.widgets.TextInput(
            attrs={'placeholder': 'Ваше имя'}
        )
    )

    password1 = forms.CharField(
        required=True,
        label='Пароль',
        widget=forms.widgets.PasswordInput(
            attrs={'placeholder': 'Пароль'}
        )
    )

    password2 = forms.CharField(
        required=True,
        label='Проверка пароля',
        widget=forms.widgets.PasswordInput(
            attrs={'placeholder': 'введите повторно пароль'}
        )
    )

    class Meta:
        fields = ['username', 'password1', 'password2']
        model = User


class AddEventForm(forms.Form):
    name = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={'placeholder': 'Название', 'id': 'new_rec_name'}
        )
    )

    address = forms.CharField(
        widget=forms.widgets.TextInput(
            attrs={'placeholder': 'Адрес', 'id': 'new_rec_address'}
        )
    )

    time = forms.DateTimeField(
        required=True,
        widget=forms.widgets.DateTimeInput(
            attrs={
                'placeholder': 'DD.MM.YYYY HH:MM',
                'id': 'new_rec_time',
                'maxlength': '16'
            },
            format="%d.%m.%Y %H:%M"
        ),
        input_formats=("%d.%m.%Y %H:%M",)
    )

    desc = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={'placeholder': 'Описание', 'id': 'new_rec_desc'}
        ),
        error_messages={'required': 'Пожалуйста, расскажите о мероприятии'},
        label='Sport'
    )

    image = forms.FileField(
        required=False,
        widget=forms.widgets.ClearableFileInput(
            attrs={
                'accept': 'image/jpeg, image/png, image/gif',
                'id': 'new_rec_img'
            }
        )
    )

    def fill_object(self):
        return Event.objects.create(
            name=self.cleaned_data['name'],
            address=self.cleaned_data['address'],
            time=self.cleaned_data['time'],
            desc=self.cleaned_data['desc']
        )
