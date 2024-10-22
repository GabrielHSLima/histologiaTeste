from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.models import User


class UsuarioCreationForm(UserCreationForm):
    nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Data de Nascimento'
    )  # Campo para a data de nascimento com widget para o seletor de data

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'nascimento', 'cargo', 'password1', 'password2']  # Adicionando os campos necessários

    
class SuporteForm(forms.ModelForm):
    class Meta:
        model = Suporte
        fields = ['problemas']  # Não inclua 'usuario' aqui

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SuporteForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        suporte = super(SuporteForm, self).save(commit=False)
        if self.user is not None:
            suporte.usuario = self.user  # Atribui o usuário
        if commit:
            suporte.save()
        return suporte
    
class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['assunto', 'mensagem']


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=254)
    new_password = forms.CharField(widget=forms.PasswordInput, label='Nova Senha')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("O e-mail não está registrado.")
        return email