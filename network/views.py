from django.shortcuts import render, get_object_or_404
from .models import *
# Create your views here.


def index(request):
	data = {"devices": Thietbi.objects.all()}
	return render(request, 'network/index.html', data)


def view_interfaces(request, pk):
	data = {"interfaces": Interfaces.objects.all().filter(matb=pk), "name": Thietbi.objects.get(matb=pk)}
	return render(request, 'network/interfaces.html', data)
