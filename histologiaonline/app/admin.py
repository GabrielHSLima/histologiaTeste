from django.contrib import admin
from .models import *
from django import forms
from django.contrib.auth.admin import UserAdmin


# Formulário de Criação de Usuário
class UsuarioCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'cargo', 'data_nascimento')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não correspondem.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Define a senha
        if commit:
            user.save()
        return user

# Registro do modelo Usuario no Admin
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):  # Certifique-se de que você está estendendo UserAdmin
    add_form = UsuarioCreationForm  # Usando o form para adição
    list_display = ('id', 'username', 'email', 'cargo', 'first_name', 'last_name', 'data_nascimento')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('cargo',)

    fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'email', 'cargo', 'data_nascimento')
        }),
        ('Senha', {
            'fields': ('password',),  # Apenas o campo de senha
        }),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Datas', {
            'fields': ('last_login',),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'cargo', 'data_nascimento', 'password1', 'password2'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(form.cleaned_data['password1'])  # Define a senha
        super().save_model(request, obj, form, change)

class ConteudosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'data_publi_autor', 'get_bibliografia_autor')
    search_fields = ('nome', 'bibliografia__autor')  # Usando a relação para buscar pelo autor
    list_filter = ('data_publi_autor',)

    def get_bibliografia_autor(self, obj):
        return obj.bibliografia.autor  # Acessando o autor através da bibliografia
    get_bibliografia_autor.short_description = 'Autor'  # Definindo o nome da coluna

# Registrando o modelo no admin
admin.site.register(Conteudos, ConteudosAdmin)

                                                                                                                                                                                       

class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'assunto', 'mensagem', 'resposta')
    search_fields = ('assunto',)

admin.site.register(Chat, ChatAdmin)

@admin.register(Suporte)
class SuporteAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'problemas')
    search_fields = ('usuario__username',)

class BibliografiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'ano_publicacao', 'editora', 'link')
    search_fields = ('titulo', 'autor')
    list_filter = ('ano_publicacao',)

# Registrando o modelo no admin
admin.site.register(Bibliografia, BibliografiaAdmin)

class RespostaInline(admin.TabularInline):
    model = Resposta  # O modelo que será exibido inline
    extra = 4  # Número de formulários vazios a serem exibidos para adicionar novas respostas

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'pergunta')  # Campos a serem exibidos na lista
    inlines = [RespostaInline]  # Adiciona as respostas como inline

@admin.register(TentativaQuiz)
class TentativaQuizAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_tentativa', 'pontuacao', 'total_perguntas')
    list_filter = ('usuario', 'data_tentativa')  # Adiciona filtros para a lista
