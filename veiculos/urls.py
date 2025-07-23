from django.urls import path
from . import views
from .views import rodar_testes_autobots

urlpatterns = [
    path('cadastrar/', views.cadastrar_autobot, name='cadastrar_autobot'),
    path('listar/', views.listar_autobots, name='listar_autobots'),
    path('rodar-testes/', rodar_testes_autobots, name='rodar_testes_autobots'),
]