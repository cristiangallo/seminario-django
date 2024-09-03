from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models import Socio, Libro


@login_required(login_url="login")
def home(request):

    args = {'socios': Socio.objects.all()}
    return render(request, "app/index.html", args)


@login_required(login_url="login")
def buscador(request):
    args = {}
    from .forms import BuscadorForm
    if request.method == "POST":
        form = BuscadorForm(request.POST)
        if form.is_valid():
            args.update({'libros': form.buscar_libros(), 'form': form})
    else:
        form = BuscadorForm(request.GET)
    args.update({'form': form})

    return render(request, "app/srch_prestamos.html", args)