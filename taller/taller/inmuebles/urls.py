from django.urls import path

from . import views

app_name = 'inmuebles'

urlpatterns = [
    path('', views.menu, name='menu'),
    path('edificios/', views.listar_edificios, name='listar_edificios'),
    path('departamentos/', views.listar_departamentos, name='listar_departamentos'),
]