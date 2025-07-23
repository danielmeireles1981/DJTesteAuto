from django.shortcuts import render, redirect
from .forms import AutobotForm
from .models import Autobot
from django.shortcuts import render
import subprocess
import sys


def cadastrar_autobot(request):
    if request.method == 'POST':
        form = AutobotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_autobots')
    else:
        form = AutobotForm()
    return render(request, 'veiculos/cadastrar_autobot.html', {'form': form})

def listar_autobots(request):
    autobots = Autobot.objects.all()
    return render(request, 'veiculos/listar_autobots.html', {'autobots': autobots})

def rodar_testes_autobots(request):
    log = ""
    if request.method == 'POST':
        result = subprocess.run(
            [sys.executable, 'manage.py', 'autobots_testes'],
            capture_output=True, text=True
        )
        log = (result.stdout or '') + (result.stderr or '')
    return render(request, 'veiculos/testes_autobots.html', {'log': log})

