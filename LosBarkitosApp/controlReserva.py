# -*- encoding: utf-8 -*-
from .models import Barca, Reserva, Control, PuntoVenta, TipoBarca
from datetime import datetime, timedelta
import json, urllib
from django.http import HttpResponse


def reserva(request, tipo, PV): # tipo Rio|Electrica|Whaly|Gold segun el tipo de barc
	#	RECOGE EL TIPO DE BARCA Y ACTUALIZA LA BDD CON LA SALIDA DE ESA BARCA
	# Busca las primeras barcas libres para escoger la que nos pide
	url = "http://127.0.0.1:8000/primera_libre/"
	respuesta = urllib.urlopen(url)
	# Contiene un JSON con las primeras barcas que llegan segun el tipo
	# [0] - rio
	# [1] - electrica
	# [2] - whaly
	# [3] - gold
	json_data = json.loads(respuesta.read())
	print '------json_data------';print json_data; print '-----------'

	# recupero la barca solicitada para salir
	tipo_barca = 1
	if tipo == 'Electrica':
		tipo_barca = 2
	elif tipo == 'Whaly':
		tipo_barca = 3
	elif tipo == 'Gold':
		tipo_barca = 4

	barca = Barca.objects.get(nombre = json_data[tipo_barca - 1 ]['nombre'])
	print '-------barca------'; print barca; print '-----------'

	try:
		h_prevista = barca.libre.isoformat()
	except Exception, e:
		h_prevista = barca.libre
		raise e

	h_prevista = barca.libre.isoformat()
	print '-------h_prevista------'; print h_prevista; print '-----------'

	barca.control += 1 # barca una vuelta mas
	barca.libre = (barca.libre + timedelta(hours = 1)).isoformat()
	print '-------barca.libre------'; print barca.libre; print '-----------'

	# SE METE EL REGISTRO EN LA TABLA DE RESERVAS
	# se recupera en numero de reserva desde la tabla control
	registro_control = Control.objects.all()[0]
	print '-------registro_control------'; print registro_control.num_reserva_whaly; print '-----------'

	if tipo == 'Rio':
		registro_control.num_reserva_rio += 1
		numero = registro_control.num_reserva_rio
	elif tipo == 'Electrica':
		registro_control.num_reserva_electrica += 1
		numero = registro_control.num_reserva_electrica
	elif tipo == 'Whaly':
		registro_control.num_reserva_whaly += 1
		numero = registro_control.num_reserva_whaly
	elif tipo == 'Gold':
		registro_control.num_reserva_gold += 1
		numero = registro_control.num_reserva_gold

	punto_venta = PuntoVenta.objects.get(codigo = PV)
	print '-------punto_venta------'; print punto_venta.nombre; print '-----------'

	t_barca = TipoBarca.objects.get(codigo = tipo_barca)
	print '-------tipo_barca------'; print t_barca.tipo; print '-----------'


	registro_reserva = Reserva(numero = numero,
							   punto_venta = punto_venta,
							   tipo_barca = t_barca,
							   hora_reserva = datetime.now().isoformat(),
							   hora_prevista = h_prevista,
							   fuera = False)

	print '-------AQUI NO LLEGA------'; print barca; print '-----------'

	try:
		barca.save()
		registro_reserva.save()
		registro_control.save()
		data = {'exito' : barca.nombre, 'hora reserva' : registro_reserva.hora_reserva,  'hora prevista' : registro_reserva.hora_prevista, 'punto venta' : registro_reserva.punto_venta.nombre, 'error' : 0}
	except Exception, e:
		data = {'exito':0, 'error': 'Error numero %s de %s' % (e.errno, e.strerror)}

	return HttpResponse(json.dumps(data), 'application/json')


# Se marca la reserva como fuera y se actualizan los horarios
def reserva_fuera(request, numero):

	try:
		reserva = Reserva.objects.get(numero = numero)
	except Reserva.DoesNotExist:
		data = {'exito' : 0, 'error' : 'Esta reserva no existe'}
		return HttpResponse(json.dumps(data), 'application/json')

	# se marca la reserva como salida
	reserva.fuera = True
	reserva.save()

	barca = reserva.tipo_barca

	# llamamos salida barca para hacer efectiva la salida de la barca
	url = 'http://127.0.0.1:8000/salida/%s' % barca.tipo
	respuesta = urllib.urlopen(url)
	json_data = json.loads(respuesta.read())

	data = {'nombre' : json_data['nombre'], 'libre' : json_data['libre']}

	return HttpResponse(json.dumps(data), 'application/json')
