from django.shortcuts import render

from .models import Departamento, Edificio


def menu(request):
    """Página principal con el menú de navegación."""
    return render(request, 'menu.html')


def listar_edificios(request):
    """Muestra en una tabla todos los edificios registrados."""
    edificios = Edificio.objects.all()
    return render(request, 'edificios_list.html', {
        'edificios': edificios,
    })


def listar_departamentos(request):
    """Muestra en una tabla todos los departamentos registrados."""
    departamentos = Departamento.objects.select_related('edificio').all()
    return render(request, 'departamentos_list.html', {
        'departamentos': departamentos,
    })