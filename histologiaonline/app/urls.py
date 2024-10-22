from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),  # Rota para a página inicial
    path('registro/', UsuarioRegisterView.as_view(), name='registro'),  # Rota para registro
    path('senha_reset/', SenhaResetView.as_view(), name='senha_reset'),
    path('login/', UsuarioLoginView.as_view(), name='login'),  # Rota para login
    path('logout/', UsuarioLogoutView.as_view(), name='logout'),  # Rota para logout
    path('suporte/', SuporteCreateView.as_view(), name='suporte'),
    path('conteudos/', ConteudosView.as_view(), name='conteudos'),
    path('chat/', GerenciarChatView.as_view(), name='chat'),
    path('atividades/', AtividadesView.as_view(), name='atividades'),
    path('gabarito/', GabaritoView.as_view(), name='gabarito'),
    path('bibliografia/', BibliografiaView.as_view(), name='bibliografia'),
]
