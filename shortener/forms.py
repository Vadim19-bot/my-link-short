from django import forms
from .models import Link
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['original_url']
        labels = {
            'original_url': 'Довге посилання',
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Електронна пошта'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']
        labels = {
            'username': "Ім'я користувача",
            'password1': "Пароль",
        }
        help_texts = {
            'username': "Обов’язкове поле. Не більше 150 символів. "
                        "Тільки літери, цифри та символи @/./+/-/_.",
            'password1': (
                "<ul>"
                "<li>Ваш пароль не повинен бути схожим на ваше ім’я або іншу особисту інформацію.</li>"
                "<li>Пароль має містити принаймні 8 символів.</li>"
                "<li>Пароль не може бути поширеним або простим.</li>"
                "<li>Пароль не може складатися лише з цифр.</li>"
                "</ul>"
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.fields.pop('password2', None)
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Ця електронна пошта вже зареєстрована.')
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        validate_password(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        label="Ім'я користувача",
        max_length=150,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message="Тільки букви, цифри та символи @/./+/-/_"
            )
        ],
        help_text="Обов'язкове поле. Не більше 150 символів. Тільки букви, цифри і символи @/./+/-/_"
    )
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


