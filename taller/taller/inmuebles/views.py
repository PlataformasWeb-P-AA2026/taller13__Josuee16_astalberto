from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .models import Departamento, Edificio
from rest_framework import viewsets, permissions
from .serializers import (
    UserSerializer,
    GroupSerializer,
    EdificioSerializer,
    DepartamentoSerializer,
)
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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class EdificioViewSet(viewsets.ModelViewSet):
    queryset = Edificio.objects.all()
    serializer_class = EdificioSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.select_related('edificio').all()
    serializer_class = DepartamentoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    