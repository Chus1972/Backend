# -*- encoding: utf-8 -*-
# funciones para el control del tickets
from django.http import HttpResponse
from .models import Viaje
from .models import PuntoVenta
from .models import TipoBarca
from .models import Vendedor
from .models import Control
import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder

# Se tiene que insertar un registro en la base de datos Viaje.
# Hay que tener en cuenta que el numero sale de Control y se 
# tiene que incrementar este numero y volverlo a grabar
def registroBarca(request, tipo, precio, pv, vend):

	regPV = PuntoVenta.objects.get(codigo = pv)
	regBarca = TipoBarca.objects.get(codigo = tipo)
	regVendedor = Vendedor.objects.get(codigo = vend)

	datosControl = Control.objects.get()
	n = datosControl.num_viaje

	reg = Viaje(numero 		= n,
				precio 		= precio,
				fecha 		= datetime.datetime.now(),
				punto_venta = regPV,
				barca 		= regBarca,
				vendedor 	= regVendedor)
	try:
		reg.save()
	except:
		data = {'error' : 1, 'tipo error' : 'Error en la grabacion del viaje'}
		return HttpResponse(json.dumps(data), 'application/json')

	# Aumento el numero de ticket y lo grabo en la bdd
	n = n + 1
	datosControl.num_viaje = n
	try:
		datosControl.save()
	except:
		data = {'error' : 1, 'tipo error' : 'Error en la grabacion del Control de datos'}
		return HttpResponse(json.dumps(data), 'application/json')

	data = {'error' : 0 ,'Numero': n, 'Precio': precio, 'Tipo Barca': regBarca.tipo}

	return HttpResponse(json.dumps(data), 'application/json')

# Devuelve un listado de los viajes segun el tipo de barca (0 para todos), punto de venta, o vendedor
def listadoViajes(request, tipo, pv, vend):
	if tipo != '0':
		filtro_tipo = TipoBarca.objects.get(codigo = tipo)
	if pv != '0':
		filtro_pv = PuntoVenta.objects.get(codigo = pv)

	if vend != '0':
		filtro_vend = Vendedor.objects.get(codigo = vend)
	filtro_fecha = datetime.now.isoformat()

	if   tipo != '0' and pv != '0' and vend != '0':
		viajes = Viaje.objects.filter(barca = filtro_tipo, punto_venta = filtro_pv, vendedor = filtro_vend)
	elif tipo != '0' and pv != '0' and vend == '0':
		viajes = Viaje.objects.filter(barca = filtro_tipo, punto_venta = filtro_pv)
	elif tipo != '0' and pv == '0' and vend != '0':
		viajes = Viaje.objects.filter(barca = filtro_tipo, vendedor = filtro_vend)
	elif tipo != '0' and pv == '0' and vend == '0':
		viajes = Viaje.objects.filter(barca = filtro_tipo)
	elif tipo == '0' and pv != '0' and vend != '0':
		viajes = Viaje.objects.filter(punto_venta = filtro_pv, vendedor = filtro_vend)
	elif tipo == '0' and pv != '0' and vend == '0':
		viajes = Viaje.objects.filter(punto_venta = filtro_pv)
	elif tipo == '0' and pv == '0' and vend != '0':
		viajes = Viaje.objects.filter(vendedor = filtro_vend)
	elif tipo == '0' and pv == '0' and vend == '0':
		viajes = Viaje.objects.filter(fecha = filtro_fecha)

	dict_viaje = []
	for viaje in viajes:
		data = {'Numero' : viaje.numero, 'Fecha' : viaje.fecha.isoformat(), 'Barca' : viaje.barca.tipo, 'Punto Venta' : viaje.punto_venta.nombre, 'Vendedor' : viaje.vendedor.nombre, 'Precio' : viaje.precio}
		dict_viaje.append(data)

	return HttpResponse(json.dumps(dict_viaje), 'application/json')

