from django.shortcuts import render

from app.models import Socio


def home(request):

    args = {'socios': Socio.objects.all()}
    return render(request, "app/index.html", args)
