# -*- encoding: utf-8 -*-
# funciones para el control del tickets
from django.http import HttpResponse
from .models import Viaje
from .models import PuntoVenta
from .models import TipoBarca
from .models import Vendedor
from .models import Control
from datetime import *
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
	today = date.today()
	if tipo != '0':
		filtro_tipo = TipoBarca.objects.get(codigo = tipo)
	if pv != '0':
		filtro_pv = PuntoVenta.objects.get(codigo = pv)

	if vend != '0':
		filtro_vend = Vendedor.objects.get(codigo = vend)

	filtro_fecha = datetime.datetime.now()
	#filtro_fecha_A = datetime.datetime.now().year
	#filtro_fecha_M = datetime.datetime.now().month
	#filtro_fecha_D = datetime.datetime.now().day

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
		viajes = Viaje.objects.filter(fecha__startswith = filtro_fecha.date()).order_by('fecha')

	dict_viaje = {}
	datos = {}
	i = 1
	for viaje in viajes:
		datos = {'numero': viaje.numero, 'fecha': datetime.datetime.strftime(viaje.fecha, "%H:%M:%S"), 'tipo':viaje.barca.tipo, 'punto_venta':viaje.punto_venta.nombre, 'nombre_vendedor':viaje.vendedor.nombre, 'precio':viaje.precio}
		dict_viaje[str(i)] = datos
		i += 1

	dict_viaje['error'] = 'no'

	try:
		jsonDict = json.dumps(dict_viaje)
	except Exception, e:
		data['error'] = e.strerror


	return HttpResponse(jsonDict, 'application/json')

