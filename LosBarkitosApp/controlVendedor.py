# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from .models import Vendedor
from .models import Viaje
import json

def ventaVendedor(request, nv):
	vend = Vendedor.objects.get(codigo = nv)
	viajes = Viaje.objects.filter(vendedor = vend)
	total = 0
	num = 0

	for v in viajes:
		total += v.precio
		num = num + 1
	datos = {'Nombre':vend.nombre, 'barcas': num, 'total': total}

	return HttpResponse(json.dumps(datos), 'application/json')

def vendedores(request):
	vend = Vendedor.objects.all()

	return HttpResponse(json.dumps(vend), 'application/json')