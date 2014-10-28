# funciones para el control del tickets
from django.http import HttpResponse
from .models import Viaje
from .models import PuntoVenta
from .models import TipoBarca
from .models import Vendedor
from .models import Control
import datetime
import json

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

# Devuelve un listado de los viajes segun el tipo de barca (todos para todos), punto de venta, o vendedor
def listadoViajes(request, tipo, pv, vend):
	if tipo == 'todos':
		filtro_tipo = ''
	else: # 1, 2 ,3 o 4 segun sea Rio, electrica, whaly o gold
		tipo_barca = TipoBarca.objects.get(codigo = tipo)
		filtro_tipo = 'barca = %o' % tipo_barca

	punto_venta = PuntoVenta.objects.get(codigo = pv)
	filtro_pv = 'punto_venta = %o' % punto_venta
	vendedor = Vendedor.objects.get(codigo = vend)
	filtro_vendedor = 'vendedor = %o' % vendedor

	viajes = Viaje.objects.filter(barca = filtro_tipo, punto_venta = filtro_pv, vendedor = filtro_vendedor)

	return HttpResponse(json.dumps(viajes), 'application/json')

