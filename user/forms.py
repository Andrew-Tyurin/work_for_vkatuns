from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name_field, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if name_field == 'username':
                field.label = 'Логин'


class RegisterUserFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2',)
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_username(self):
        username = self.cleaned_data['username']
        if username == "AnonymousUser":
            raise ValidationError('Недопустимый логин')
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name.isalpha():
            return first_name
        raise ValidationError('Имя должно состоять из букв')

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name.isalpha():
            return last_name
        raise ValidationError('Фамилия должна состоять из букв')
