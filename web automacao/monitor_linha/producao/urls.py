from django.urls import path
from . import views

urlpatterns = [
    path("paradas/", views.tabela_paradas, name="tabela_paradas"),
    path("registrar-motivo/", views.registrar_motivo, name="registrar_motivo"),
    path('exportar/<str:filtro>/', views.exportar_csv, name='exportar_csv'),
]
