from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    Aluno = 'aluno'
    Professor = 'professor'

    CARGO_CHOICES = [
        (Aluno, 'Aluno'),
        (Professor, 'Professor'),
    ]

    data_nascimento = models.DateField(verbose_name="Data de Nascimento", blank=True, null=True)
    cargo = models.CharField(max_length=50, choices=CARGO_CHOICES, default=Aluno, verbose_name="Cargo", blank=True, null=True)
    chat = models.ForeignKey('Chat', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Se o cargo for 'Professor', o usuário será superusuário
        if self.cargo == self.Professor:
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False

        super().save(*args, **kwargs)

class Bibliografia(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=100)
    ano_publicacao = models.IntegerField()
    editora = models.CharField(max_length=100, blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.titulo

class Conteudos(models.Model):
    nome = models.CharField(max_length=255)
    data_publi_autor = models.DateField()
    curiosidades = models.TextField(blank=True, null=True)
    tema_especifico = models.CharField(max_length=255, blank=True, null=True)
    bibliografia = models.ForeignKey(Bibliografia, on_delete=models.CASCADE, related_name='conteudos')


    def __str__(self):
        # Retorna o nome do conteúdo e o autor da bibliografia
        return f"{self.nome} - Autor da Bibliografia: {self.bibliografia.autor if self.bibliografia else 'N/A'}"
    
class Chat(models.Model):
    assunto = models.CharField(max_length=255)
    mensagem = models.TextField()
    resposta = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.assunto

class Suporte(models.Model):
    problemas = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Suporte {self.id} - {self.usuario}"

class Quiz(models.Model):
    titulo = models.CharField(max_length=255)  # Título do quiz
    pergunta = models.CharField(max_length=255)  # Texto da pergunta
   
    def __str__(self):
        return self.titulo

class Resposta(models.Model):
    Quiz = models.ForeignKey( Quiz , on_delete=models.CASCADE, related_name='respostas')  # Pergunta relacionada
    texto = models.CharField(max_length=255)  # Texto da resposta
    ordem = models.IntegerField()  # Ordem de exibição
    correta = models.BooleanField(default=False)  # Indica se a resposta é correta

    def __str__(self):
        return self.texto

class TentativaQuiz(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Usuário que fez a tentativa
    data_tentativa = models.DateTimeField(auto_now_add=True)  # Data da tentativa
    pontuacao = models.IntegerField()  # Pontuação obtida na tentativa
    total_perguntas = models.IntegerField()  # Total de perguntas do quiz

    def __str__(self):
        return f"Tentativa de {self.usuario} em {self.data_tentativa} - Pontuação: {self.pontuacao}"