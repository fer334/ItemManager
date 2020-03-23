from django import forms

# models
from django.contrib.auth.validators import UnicodeUsernameValidator

from login.models import Usuario

from login.Register import crear_usuario


class RegisterForm(forms.ModelForm):
    """Formulario del usuario."""

    class Meta:
        """Form settings."""

        model = Usuario
        fields = ('username', 'email', 'password', 'pass_confirmation',
                  'first_name', 'last_name')
        widgets = {
            'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        """
        Constructor de clase, se modifican algunos atributos predefinidos
        :param args: args por defecto
        :param kwargs: kwargs por defecto
        """
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    pass_confirmation = forms.CharField(
        label='Confirmar contraseña',
        min_length=6,
        max_length=70,
        widget=forms.PasswordInput(),
    )

    def clean_email(self):
        """Comprueba si el usuario es unico"""
        email = self.cleaned_data['email']
        email_taken = Usuario.objects.filter(email=email).exists()
        if email_taken:
            raise forms.ValidationError('El email ya esta en registrado.')
        return email

    def clean(self):
        """Verifica que la igualdad entre contraseñas."""
        data = super().clean()

        password = data['password']
        pass_confirmation = data['pass_confirmation']

        if password != pass_confirmation:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return data

    def save(self):
        """Create user and profile."""
        data = self.cleaned_data

        user = crear_usuario(data['email'], data['password'])

        data.pop('pass_confirmation')
        data.pop('password')

        data['localId'] = user['localId']
        data['is_active'] = False

        if Usuario.objects.count() == 0:
            data['is_superuser'] = True
            data['is_active'] = True

        nuevo_usuario = Usuario(**data)
        nuevo_usuario.save()


class UpdateUserForm(forms.ModelForm):
    """Formulario del usuario."""

    username_validator = UnicodeUsernameValidator()
    #: Campo para la modificacion del nombre de Usuario
    username = forms.CharField(
        label='Nombre de Usuario',
        min_length=3,
        max_length=150,
        required=True,
        help_text='Requerido. 150 caracteres o menos. Solamente letras, digitos y @/./+/-/_',
        validators=[username_validator],
    )

    field_order = ('username', 'first_name', 'last_name')

    class Meta:

        """Form settings."""

        model = Usuario
        fields = ('first_name', 'last_name')

    def update(self, key):
        """Update user and profile."""
        data = self.cleaned_data
        Usuario.objects.filter(username=key).update(**data)

    def clean_username(self):
        """Comprueba si el usuario es unico"""
        username = self.cleaned_data['username']
        user_taken = Usuario.objects.filter(username=username)
        print(user_taken.count() < 1)
        print(user_taken[0].id != self.instance.id)
        if user_taken.count() > 0:
            if user_taken[0].id != self.instance.id:
                pass
        else:
            raise forms.ValidationError('El nombre de usuario no esta disponible')
        return username
