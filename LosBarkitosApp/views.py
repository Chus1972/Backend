# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from .models import Barca, Control, Reserva, TipoBarca, Viaje
import json, urllib
from datetime import datetime, time
import MySQLdb

# Funciones para el control de las barcas
'''
JSON CON LAS BARCAS QUE ESTAN POR LLEGAR POR ORDEN DE LLEGADA
'''
def llegada(request, tipo):

	if tipo == 'Rio':
		tipo_barca = 1
	elif tipo == 'Electrica':
		tipo_barca = 2
	elif tipo == 'Whaly':
		tipo_barca = 3
	elif tipo == 'Gold':
		tipo_barca = 4
	else:
		tipo_barca = 0

	# Se recoge la lista de barcas fuera por orden de llegada y segun el tipo de barca
	if tipo_barca == 0:
		listaBarcas = Barca.objects.all().order_by('tipo_barca','libre', 'control', 'codigo',)
	else:
		listaBarcas = Barca.objects.filter(tipo_barca = tipo_barca).order_by('tipo_barca','libre', 'control', 'codigo',)

	indice = 1
	data = {}
	dict_data = {}

	for barca in listaBarcas:
		tipo = barca.tipo_barca
		if tipo != 0:
			regTipo = TipoBarca.objects.get(codigo = tipo_barca)

		if barca.libre == None: # quiere decir que la barca esta libre
			hora = 'libre'
		else:
			hora = datetime.time(barca.libre).isoformat()

		data = {'Tipo' : regTipo.tipo, 'Nombre' : barca.nombre, 'libre' : hora, 'vueltas' : barca.control}
		dict_data[str(indice)] = data
		indice += 1

	return HttpResponse(json.dumps(dict_data), "application/json")

'''
JSON CON LAS BARCAS QUE ESTAN FUERA POR ORDEN DE LLEGADA
'''
def barcasFuera(request):
	lista_fuera = Barca.objects.all().order_by('libre')

	data = {}
	lista_data = []
	for barca in lista_fuera:
		if barca.libre != None:
			tipo = barca.tipo_barca
			hora = datetime.time(barca.libre).isoformat()
			data = {'Nombre' : barca.nombre, 'Tipo' : tipo.tipo, 'libre' : hora}
			lista_data.append(data)

	return HttpResponse(json.dumps(lista_data), "application/json")

'''
DEVUELVE UN JSON CON LA PRIMERA BARCA DISPONIBLE SEGUN TIPO BARCA
'''
def primeraLibre(request):
	lista = {}
	primera_rio = Barca.objects.filter(tipo_barca = 1).order_by('control', 'libre', 'codigo')[0]
	primera_electrica = Barca.objects.filter(tipo_barca = 2).order_by('control', 'libre', 'codigo')[0]
	primera_whaly = Barca.objects.filter(tipo_barca = 3).order_by('control', 'libre', 'codigo')[0]
	primera_gold = Barca.objects.filter(tipo_barca = 4).order_by('control', 'libre')[0]

	try:
		rio = {'nombre' : primera_rio.nombre, 'libre' : datetime.time(primera_rio.libre).isoformat()}
	except TypeError:
		rio = {'nombre' : primera_rio.nombre, 'libre' : 'libre'}

	try:
		electrica = {'nombre' : primera_electrica.nombre, 'libre' : datetime.time(primera_electrica.libre).isoformat()}
	except TypeError:
		electrica = {'nombre' : primera_electrica.nombre, 'libre' : 'libre'}

	try:
		whaly = {'nombre' : primera_whaly.nombre, 'libre' : datetime.time(primera_whaly.libre).isoformat()}
	except TypeError:
		whaly = {'nombre' : primera_whaly.nombre, 'libre' : 'libre'}
	try:
		gold = {'nombre' : primera_gold.nombre, 'libre' : datetime.time(primera_gold.libre).isoformat()}
	except TypeError:
		gold = {'nombre' : primera_gold.nombre, 'libre' : 'libre'}

	lista["rio"] 	   = rio
	lista["electrica"] = electrica
	lista["whaly"]	   = whaly
	lista["gold"] 	   = gold

	return HttpResponse(json.dumps(lista), 'application/json')

def salidaBarca(request, tipo): # tipo Rio|Electrica|Whaly|Gold segun el tipo de barc
	#	RECOGE EL TIPO DE BARCA Y ACTUALIZA LA BDD CON LA SALIDA DE ESA BARCA
		# recupero la barca solicitada para salir

	tipo_barca = 1

	if tipo == 'Electrica':
		tipo_barca = 2
	elif tipo == 'Whaly':
		tipo_barca = 3
	elif tipo == 'Gold':
		tipo_barca = 4

	barca = Barca.objects.filter(tipo_barca = tipo_barca).order_by('libre', '-control')[0]

	# si "libre" = None -> barca parada
	# si "libre" != None y control == 0 -> barca circulando pero no tiene reservas
	if barca.control == 0 and barca.libre == None:
		barca.libre = datetime.now().isoformat()
	elif barca.control == 0 and barca.libre != None: # esta opcion no se puede dar
		pass
	elif barca.control > 0:
		barca.control -= 1

	try:
		barca.save()
		data = {'nombre' : barca.nombre, 'libre' : datetime.time(barca.libre).isoformat()}
	except TypeError: # puede decir que barca.libre = None y fallaria
		barca.save()
		data = {'nombre' : barca.nombre, 'libre' : 'None'}

	return HttpResponse(json.dumps(data), 'application/json')

# ESTE METODO RECOGE UNA LLEGADA DE UNA BARCA SEGUN SU TIPO Y DEVUELVE EL CODIGO DE LA BARCA QUE LLEGA
# tipo en este metodo es un string con el nombre del tipo
def llegadaBarca(request, tipo):

	#if hayReservas:
	# RECOGE EL TIPO DE BARCA Y ACTUALIZA LA BDD CON LA LLEGADA DE LA BARCA
	url = "http://127.0.0.1:8000/llegada"
	respuesta = urllib.urlopen(url)
		# Contiene un JSON con las barcas que llegan por orden de llegada y segun el tipo
	# [0] - rio
	# [1] - electrica
	# [2] - whaly
	# [3] - gold
	json_data = json.loads(respuesta.read())

	# Recorre el JSON para encontrar la primera barca con libre<>None y segun el tipo
	for barca in json_data:
		if (barca['libre'] != 'libre' and  barca['Tipo'] == tipo):
 			break

 	# tengo la barca que ha llegado
 	barcaBD = Barca.objects.get(nombre = barca['Nombre'])

 	hay_reservas = barcaBD.control > 0

	if not hay_reservas:
		barcaBD.libre = None

	try:
		barcaBD.save()
		data = {'exito' : barcaBD.nombre, 'error' : 0}
	except Exception, e:
		data = {'exito' : 0, 'error': 'Error numero %s de %s' % (e.errno, e.strerror)}

	return HttpResponse(json.dumps(data), 'application/json')


def noDisponible(request, num_barca):
	barca = Barca.objects.get(codigo = num_barca)
	barca.control = 2 # barca averiada
	barca.libre = None

	try:
		barca.save()
		data = {'exito':barca.codigo, 'error':0}
	except Exception, e:
		data = {'exito':0, 'error': 'Error numero %s de %s' % (e.errno, e.strerror)}

	return HttpResponse(json.dumps(data), 'application/json')

def disponible(request, num_barca):
	barca = Barca.objects.get(codigo = num_barca)
	barca.control = 0 # barca averiada
	barca.libre = None

	try:
		barca.save()
		data = {'exito':barca.codigo, 'error':0}
	except Exception, e:
		data = {'exito':0, 'error': 'Error numero %s de %s' % (e.errno, e.strerror)}

	return HttpResponse(json.dumps(data), 'application/json')


# Resetea tanto la tabla Barca como la tabla de Reservas y los campos de control adecuados
def resetear(request):
	barcas = Barca.objects.all()
	control = Control.objects.all()[0]
	reservas = Reserva.objects.all()

	try:
		for barca in barcas:
			barca.control = 0
			barca.libre = None
			barca.save()
		#for control in controls
		control.num_viaje = 0
		control.num_reserva = 0
		control.libre = None
		control.reserva_rio = 0
		control.reserva_electrica = 0
		control.reserva_whaly = 0
		control.reserva_gold = 0
		control.control1 = 0
		control.save()

		reservas.delete()

		data = {'exito' : 'ok', 'error' : 0}
	except Exception, e:
		data = {'exito':0, 'error': 'Error numero %s de %s' % (e.errno, e.strerror)}


	return HttpResponse(json.dumps(data), 'application/json')

def totalBarcas(request):
	#tipoRio 		= TipoBarca.objects.get(codigo = 1)
	#tipoElectrica	= TipoBarca.objects.get(codigo = 2)
	#tipoWhaly		= TipoBarca.objects.get(codigo = 3)
	#tipoGold		= TipoBarca.objects.get(codigo = 4)

	dia = datetime.now().strftime("%d");print dia
	mes = datetime.now().strftime("%m");print mes
	ano = datetime.now().strftime("%Y"); print ano

	db = MySQLdb.connect(user = 'b17e70697e2374', db='heroku_c71c74c67cde020', passwd='3eaf2e91', host='eu-cdbr-west-01.cleardb.com')
	cursor = db.cursor()
	llamada = 'SELECT count(*) FROM LosBarkitosApp_viaje where barca_id=1 and year(fecha)=%s  and month(fecha)=%s and day(fecha)=%s' % (ano, mes, dia)
	cursor.execute(llamada)
	RIOS = [row[0] for row in cursor.fetchall()]
	llamada = 'SELECT count(*) FROM LosBarkitosApp_viaje where barca_id=2 and year(fecha)=%s  and month(fecha)=%s and day(fecha)=%s' % (ano, mes, dia)
	ELECTRICAS = [row[0] for row in cursor.fetchall()]
	llamada = 'SELECT count(*) FROM LosBarkitosApp_viaje where barca_id=3 and year(fecha)=%s  and month(fecha)=%s and day(fecha)=%s' % (ano, mes, dia)
	cursor.execute(llamada)
	WHALYS = [row[0] for row in cursor.fetchall()]
	llamada = 'SELECT count(*) FROM LosBarkitosApp_viaje where barca_id=4 and year(fecha)=%s  and month(fecha)=%s and day(fecha)=%s' % (ano, mes, dia)
	GOLDS = [row[0] for row in cursor.fetchall()]

	data = {'rio' : RIOS, 'electrica' : ELECTRICAS, 'whaly' : WHALYS, 'gold' : GOLDS}

	return HttpResponse(json.dumps(data), 'application/json')