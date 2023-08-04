from django.shortcuts import get_object_or_404, render
from .models import Bloque, Sitio
from django.db.models import Q

# Create your views here.

def home(request):
    bloques = Bloque.objects.all()
    return render(request, 'home.html', {'bloques': bloques})

def bloque(request, bloque_id):
    bloque = get_object_or_404(Bloque, id=bloque_id)
    sitios = bloque.sitio_set.all()
    return render(request, 'bloque.html', {'bloque': bloque, 'sitios': sitios })

def listadoBloques(request):
    bloques = Bloque.objects.all()
    return render(request, 'listadoBloques.html', {'bloques': bloques})

def resultados_busqueda(request):
    query = request.GET.get('q')

    if query:
        # Realizar la consulta en la base de datos
        resultados_bloques = Bloque.objects.filter(
            Q(nombre__icontains=query) |  # Busca en el campo "nombre"
            Q(funciones__icontains=query) |  # Busca en el campo "funciones"
            Q(descripcion__icontains=query)  # Busca en el campo "descripcion"
        ).distinct()  # Agregamos .distinct() para evitar duplicados

        resultados_sitios = Sitio.objects.filter(
            Q(nombre__icontains=query) |  # Busca en el campo "nombre"
            Q(descripcion__icontains=query) |  # Busca en el campo "descripcion"
            Q(aulas__icontains=query)  # Busca en el campo "aulas"
        ).distinct()  # Agregamos .distinct() para evitar duplicados

    else:
        resultados_bloques = None
        resultados_sitios = None

    return render(request, 'busqueda.html', {
        'resultados_bloques': resultados_bloques,
        'resultados_sitios': resultados_sitios,
        'query': query,
    })