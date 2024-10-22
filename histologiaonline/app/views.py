from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class Index(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')  # URL para a página de login

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')  # Redireciona para a página de login caso o usuário não esteja autenticado


class UsuarioRegisterView(View):
    template_name = 'autenticacao/registro.html'  # Template para registro

    def get(self, request):
        form = UsuarioCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            try:
                # Verificar se o usuário já existe (pelo nome de usuário ou email)
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']

               

                # Se o formulário for válido e o usuário não existir, salvar o novo usuário
                user = form.save()  # Salva o novo usuário
                login(request, user)  # Faz o login automático
                if user.is_superuser:
                    return redirect('index')  # Redireciona para a página inicial do admin
                else:
                    return redirect('index')  # Redireciona para a página inicial após o registro

            except ValidationError as e:
                # Se ocorrer algum erro de validação durante o salvamento do usuário
                messages.error(request, f'Ocorreu um erro ao tentar salvar o usuário: {str(e)}')
                return render(request, self.template_name, {'form': form})

            except Exception as e:
                # Captura qualquer outra exceção
                messages.error(request, f'Ocorreu um erro inesperado: {str(e)}')
                return render(request, self.template_name, {'form': form})
        else:
            # Se o formulário não for válido, exibe os erros de validação
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            
            # Mensagem personalizada sobre os requisitos da senha
            if 'password1' in form.errors:
                password_error_message = "A senha não atende aos requisitos necessários. "
                password_error_message += "Ela deve ter pelo menos 8 caracteres, incluir números, letras maiúsculas e minúsculas, e um caractere especial."
                messages.error(request, password_error_message)
            
            # Mensagem para o caso de nome de usuário já existente
            if 'username' in form.errors:
                username_error_message = "O nome de usuário já está em uso."
                messages.error(request, username_error_message)

            # Mensagem para o caso de e-mail já registrado
            if 'email' in form.errors:
                email_error_message = "O e-mail já está cadastrado."
                messages.error(request, email_error_message)

            return render(request, self.template_name, {'form': form})
            
class UsuarioLoginView(View):
    template_name = 'autenticacao/login.html'  # Template de login

    def get(self, request):
        # Verifica se o usuário já está logado
        if request.user.is_authenticated:
            return redirect('index')  # Redireciona para a página inicial se já estiver logado

        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Faz o login do usuário
                return redirect('index')  # Redireciona para a página inicial após o login
        return render(request, self.template_name, {'form': form})

class UsuarioLogoutView(View):
    def get(self, request):
        logout(request)  # Faz o logout do usuário
        return redirect('login')  # Redireciona para a página de login após o logout
    
class SenhaResetView(View):
    template_name = 'autenticacao/senha_reset.html'

    def get(self, request):
        # Exibe o formulário vazio ao acessar a página de reset de senha
        form = PasswordResetForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # Processa o formulário quando o usuário envia os dados
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                # Usa o modelo de usuário personalizado
                User = get_user_model()
                user = User.objects.get(email=email)
                user.set_password(form.cleaned_data['new_password'])  # Define a nova senha
                user.save()  # Salva o usuário com a nova senha
                messages.success(request, 'Senha redefinida com sucesso!')  # Adiciona uma mensagem de sucesso
                return redirect('login')  # Redireciona para a página de login após o sucesso
            except User.DoesNotExist:
                form.add_error('email', 'O e-mail não está registrado.')  # Adiciona erro se não encontrar o usuário
        return render(request, self.template_name, {'form': form})
    
class SuporteCreateView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        form = SuporteForm(user=request.user)  # Passa o usuário para o formulário
        return render(request, 'suporte.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SuporteForm(request.POST, user=request.user)  # Passa o usuário para o formulário
        if form.is_valid():
            form.save()  # O usuário será salvo automaticamente pelo método save do formulário
            messages.success(request, 'Mensagem de suporte enviada com sucesso!')  # Exibe uma mensagem de sucesso
            return redirect('suporte')  # Substitua 'suporte' pela URL de sucesso real
        return render(request, 'suporte.html', {'form': form})

class ConteudosView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        conteudos = Conteudos.objects.all()  # Obtém todos os conteúdos do banco de dados
        return render(request, 'conteudos.html', {'conteudos': conteudos})
    
class GerenciarChatView(LoginRequiredMixin,View):
    def get(self, request):
        form = ChatForm()
        chats = Chat.objects.all()
        return render(request, 'chat.html', {'form': form, 'chats': chats})

    def post(self, request):
        form = ChatForm(request.POST)
        if form.is_valid():
            chat_instance = form.save(commit=False)  # Não salva ainda
            resposta = self.obter_resposta(chat_instance.mensagem)
            chat_instance.resposta = resposta  # Define a resposta predefinida
            chat_instance.save()  # Agora salva a nova mensagem com resposta
            return redirect('chat')
        
        chats = Chat.objects.all()
        return render(request, 'chat.html', {'form': form, 'chats': chats})


class AtividadesView(LoginRequiredMixin, View):
    def get(self, request):
        # Busca o quiz e suas respostas
        quizzes = Quiz.objects.all()  # Altere conforme necessário
        return render(request, 'atividades.html', {'perguntas': quizzes, 'score': None, 'total': None})

    def post(self, request):
        usuario = request.user
        score = 0
        total = 0
        
        # Busca todas as perguntas e suas respostas
        quizzes = Quiz.objects.all()  # Altere conforme necessário
        for quiz in quizzes:
            resposta_id = request.POST.get(f'pergunta_{quiz.id}')  # Certifique-se que o nome do campo está correto
            if resposta_id:
                total += 1
                # Verifica se a resposta é correta
                try:
                    resposta = Resposta.objects.get(id=resposta_id, Quiz_id=quiz)
                    if resposta.correta:
                        score += 1
                except Resposta.DoesNotExist:
                    continue
        
        # Salva a tentativa do quiz
        TentativaQuiz.objects.create(usuario=usuario, pontuacao=score, total_perguntas=total)
        messages.success(request, f'Atividade concluída com sucesso! Você acertou {score} de {total} questões.')
        return redirect('atividades')
        
     
class BibliografiaView(LoginRequiredMixin,View):
    def get(self, request):
        bibliografias = Bibliografia.objects.all()  # Obtém todas as bibliografias
        return render(request, 'bibliografia.html', {'bibliografias': bibliografias})
    


class GabaritoView(View):
    template_name = 'gabarito.html'

    def get(self, request, *args, **kwargs):
        # Obter todos os quizzes
        quizzes = Quiz.objects.all()
        respostas_usuario = request.session.get('respostas', {})

        resultados = []
        for quiz in quizzes:
            respostas = quiz.respostas.all().order_by('ordem')  # Garantir que a ordem das respostas esteja correta
            resposta_usuario = respostas_usuario.get(str(quiz.id), None)
            resposta_correta = respostas.filter(correta=True).first()

            resultado = {
                'quiz': quiz,
                'respostas': respostas,
                'resposta_usuario': resposta_usuario,
                'resposta_correta': resposta_correta,
                'acertou': resposta_usuario == resposta_correta.id if resposta_usuario else False
            }
            resultados.append(resultado)

        context = {
            'resultados': resultados
        }

        return render(request, self.template_name, context)