from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date
from app.models import Socio, Libro, Prestamo


def devolver_libro(request, id_prestamo):
    from .forms import BuscadorForm, DevolucionForm

    prestamo = Prestamo.objects.get(id=id_prestamo)
    if request.method == 'POST':
        form_prestamo = DevolucionForm(request.POST)
        if form_prestamo.is_valid():
            prestamo = form_prestamo.save()
    else:
        form_prestamo = DevolucionForm(instance=prestamo, initial={'recibio': request.user.bibliotecario})

    alerta = True if prestamo.fecha_max_dev < date.today() else False

    args = {"form": BuscadorForm(), 'form_prestamo': form_prestamo, 'alerta': alerta, 'prestamo': prestamo}


    return render(request, "app/devolver-libro.html", args)


def prestar_libro(request):
    from .forms import BuscadorForm, PrestamoForm

    if request.method == "POST":
        form_prestamo = PrestamoForm(request.POST)
        if form_prestamo.is_valid():
            prestamo = form_prestamo.save()


    else:
        form_prestamo = PrestamoForm(
            initial={'entrego': request.user.bibliotecario})

    args = {"form": BuscadorForm(), 'form_prestamo': form_prestamo}
    return render(request, "app/prestar-libro.html", args)


def login_view(request, next_page="/"):
    from django.contrib import messages
    from django.contrib.auth import authenticate
    from django.contrib.auth import login
    from django.http import HttpResponseRedirect, HttpResponse

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['bienvenida'] = f"Bienvenido, {user.username}"
            return HttpResponseRedirect(next_page)
        else:
            messages.add_message(request, messages.ERROR, "¡Credenciales inválidas! El usuario y/o la contraseña no coinciden.")
    return render(request, "app/login_register.html")


@login_required(login_url="login")
def home(request):
    args = {}
    from .forms import BuscadorForm
    if request.method == "POST":
        form = BuscadorForm(request.POST)
    else:
        form = BuscadorForm(request.GET)

    form.is_valid()
    args['form'] = form
    args['objetos'] = form.buscar()
    return render(request, "app/index.html", args)


@login_required(login_url="login")
def buscador(request):
    args = {}
    from .forms import BuscadorForm
    if request.method == "POST":
        form = BuscadorForm(request.POST)
        if form.is_valid():
            args.update({'objetos': form.buscar_libros(), 'form': form})
    else:
        form = BuscadorForm(request.GET)
    args.update({'form': form})

    return render(request, "app/index.html", args)


def libros_prestados(request):
    from .models import Prestamo
    from .forms import BuscadorForm

    args = {
        'objetos': Prestamo.objects.filter(fecha_dev__isnull=True),
        'form': BuscadorForm(request.GET)}


    return render(request, "app/index.html", args)
