from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bloque/<int:bloque_id>/', views.bloque, name='bloque'),
    path('listado_de_bloques', views.listadoBloques, name='listadoBloques' ),
    path('resultados/', views.resultados_busqueda, name='resultados_busqueda'),
]