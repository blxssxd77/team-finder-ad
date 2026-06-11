from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm

from team_finder.validators import validate_github_url

from .models import User
from .utils import normalize_phone, validate_phone


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(
                self.request,
                username=email,
                password=password,
            )
            if self.user_cache is None:
                raise forms.ValidationError('Неверный email или пароль')
        return cleaned_data

    def get_user(self):
        return self.user_cache


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'avatar', 'about', 'phone', 'github_url')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not validate_phone(phone):
            raise forms.ValidationError(
                'Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX',
            )
        phone = normalize_phone(phone)
        qs = User.objects.filter(phone=phone)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Этот номер телефона уже используется')
        return phone

    def clean_github_url(self):
        return validate_github_url(self.cleaned_data.get('github_url', ''))


class CustomPasswordChangeForm(PasswordChangeForm):
    pass
