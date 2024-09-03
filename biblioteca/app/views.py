from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models import Socio, Libro


@login_required(login_url="login")
def home(request):

    args = {'socios': Socio.objects.all()}
    return render(request, "app/index.html", args)

@login_required(login_url="login")
def buscador(request):
    from .forms import BuscadorForm

    form = BuscadorForm(request.GET)
    nombre_libro = request.GET.get('libro')
    libros = Libro.objects.filter(titulo__icontains=nombre_libro)
    args = {'libros': libros, 'form': form}

    return render(request, "app/srch_prestamos.html", args)