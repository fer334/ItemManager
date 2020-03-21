from django import forms

#models
from login.models import Usuario

from login.Register import crear_usuario


class RegisterForm(forms.Form):
	"""
	Formulario para el Usuario
	"""

	username = forms.CharField(
		min_length=3, 
		max_length=50,
	)
	password = forms.CharField(
		min_length=6,
		max_length=70, 
		widget= forms.PasswordInput()
	)
	password_confirmation = forms.CharField(
		min_length=6,
		max_length=70,
		widget=forms.PasswordInput()
	)
    
	first_name = forms.CharField(min_length=4, max_length=50)
	last_name = forms.CharField(min_length=4, max_length=50)

	email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput()
    )

	def clean_username(self):
		"""Comprueba si el usuario es unico"""
		username = self.cleaned_data['username']
		username_taken = Usuario.objects.filter(username=username).exists()
		if username_taken:
			raise forms.ValidationError('El nombre de Usuario ya esta en uso.')
		return username

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
		password_confirmation = data['password_confirmation']

		if password != password_confirmation:
			raise forms.ValidationError('Las contraseñas no coinciden.')

		return data


	def save(self):
		"""Create user and profile."""
		data = self.cleaned_data

		user = crear_usuario(data['email'],data['password'])

		data.pop('password_confirmation')
		data.pop('password')
		
		data['localId'] = user['localId']
		data['is_active'] = False

		if (Usuario.objects.count() == 0):
			data['is_superuser'] = True
			data['is_active'] = True

		nuevo_usuario = Usuario(**data)
		nuevo_usuario.save()

