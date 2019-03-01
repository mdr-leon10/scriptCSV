import csv
from datetime import datetime, timedelta
import re

CRITICAL = 'critical'
WINDOWS = 'windows'
NORESPONSE = 'no response from remote host'
titulos = ['status not found', 'correlacion', 'n/a']
sistemasOperativosSSH = ['unix', 'linux', 'solaris', 'aix']
categoria = ['disk', 'disco', 'proceso uptime', 'interface index']

#Obtiene el día del evento a partir de la hora dada por parametro
def obtenerDia(horaInicial):
	día = ''
	splitF = horaInicial.split('T')
	fecha = splitF[0].split('-')
	dia = fecha[2]
	return dia

#Obtiene la hora inicial del evento a partir de la hora dada por parametro
def obtenerHoraInicial(horaInicial):
	hora = ''
	splitF = horaInicial.split('T')
	fecha = splitF[1].split('.')
	hora = fecha[0]
	return hora

#Obtiene la hora final del evento a partir de la hora dada por parametro
def obtenerHoraFinal(horaFinal):
	hora = ''
	splitF = horaFinal.split('T')
	fecha = splitF[1].split('.')
	hora = fecha[0]
	return hora

#Obtiene la franja horaria a la que pertenece el evento a partir de la hora dada por paráametro
def obtenerFranjaHoraria(horaInicial, fechaDia):
	string2 = horaInicial.split('.')
	string = string2[0].split(',')
	hora = datetime.strptime(string[0], '%Y-%m-%dT%H:%M:%S')
	horaComp = datetime.strptime(fechaDia + ' ' + '00:00:00', '%Y-%m-%d %H:%M:%S')
	franjaH = ' '
	i = 0
	while i<24:
		if(horaComp <= hora and (horaComp + timedelta(hours = 1)) > hora):
			franjaH = str(horaComp).split(' ')[1] + ' hasta ' + str(horaComp + timedelta(minutes = 59, seconds = 59)).split(' ')[1]
			i = 24
		else:
			horaComp = horaComp + timedelta(hours = 1)
		# print (str(hora) + ' franja: ' + franjaH)
	return franjaH

#Obtiene las maquinas wmi para los eventos criticos
def obtenerWmi(severity, objeto, titulo, descripcion, ciType, net):
	foundMatch = False
	objectLow = objeto.lower()
	descripcionLow = descripcion.lower()
	tituloLow = titulo.lower()
	ciTypeLow = ciType.lower()
	if(severity.lower() == CRITICAL and net != 'SI'): 
		if (objectLow.find(WINDOWS) != -1):
			if (descripcionLow.find(NORESPONSE) != -1):
				foundMatch = True
			else: 
				for tit in titulos:
					if (tituloLow.find(tit.lower()) != -1):
						foundMatch = True
		
	if (severity.lower() == CRITICAL and objectLow.find(WINDOWS) == -1 and ciTypeLow.find(WINDOWS) != -1):
		if (descripcionLow.find(NORESPONSE) != -1):
				foundMatch = True
		else: 
			for tit in titulos:
				if (tituloLow.find(tit.lower()) != -1):
					foundMatch = True

	if (foundMatch):    
		return 'SI'
	else:
		return ''

#Obtiene las maquinas de net para los eventos criticos
def obtenerNet(severity, nodeHint, title, descripcion):
	found = False
	titleLower = title.lower()
	descripcionLow = descripcion.lower()
	nodeHintLow = nodeHint.lower()
	if (severity.lower() == CRITICAL):
		with open('maquinasNetbios.csv' , 'r') as maquina:
			for line in maquina:
				linea = line.lower()
				if(linea.find(nodeHintLow)!=-1):
					if(descripcionLow.find(NORESPONSE) != -1):
						found = True
						break
					else:
						for tit in titulos:
							if(titleLower.find(tit.lower()) != -1):
								found = True
								break
						if (found == True):
							break
	if (found == True):
		return 'SI'
	else:
		return ' '

#Obtiene las maquinas ssh para los eventos criticos
def obtenerSsh(severity, objeto, titulo, descripcion, ciType, net, wmi):
	objetoLow = objeto.lower()
	tituloLow = titulo.lower()
	descripcionLow = descripcion.lower()
	ciTypeLow = ciType.lower()
	foundMatch = False
	if (severity.lower() == CRITICAL and net != 'SI' and wmi != 'SI'):
		foundMatch = False 
		for SO in sistemasOperativosSSH:
			if (objetoLow.find(SO.lower()) != -1):
				if (descripcionLow.find(NORESPONSE) != -1):
					foundMatch = True
					break
				else: 
					for tit in titulos:  
						if (tituloLow.find(tit.lower()) != -1):
							foundMatch = True
							break
			if (severity.lower() == CRITICAL and objetoLow.find(SO) == -1 and ciTypeLow.find(SO) != -1):
				if (descripcionLow.find(NORESPONSE) != -1):
					foundMatch = True
				else: 
					for tit in titulos:
						if (tituloLow.find(tit.lower()) != -1):
							foundMatch = True

	if (foundMatch == True):
		return 'SI'
	else :
		return ''

#Obtiene las maquinas no identificadas para los eventos criticos
def obtenerNoIden(severity, titulo, objeto, ciType, descripcion):
	foundit = False
	tituloLow = titulo.lower()
	objetoLow = objeto.lower()
	ciTypeLow = ciType.lower()
	descripcionLow = descripcion.lower()
	sePuede = True

	if(ciTypeLow == ' ' and severity.lower() == CRITICAL and objetoLow.find(WINDOWS) == -1):
		for so in sistemasOperativosSSH:
			soLow = so.lower()
			if (objetoLow.find(soLow) != -1):
				sePuede = False

		if(sePuede == True):
			if (descripcionLow.find(NORESPONSE) != -1):
				foundit = True 
			else:
				for tit in titulos:
					if(tituloLow.find(tit.lower())!= -1):
						foundit = True 
	if (foundit == True):
		return 'SI'
	else:
		return ' '

#Obtiene los counters para los eventos criticos
def obtenerCounter(severity, titulo):
	found =' '
	titLow = titulo.lower()
	if(severity.lower() == CRITICAL):
		if (titLow.find('counters in error') != -1):
			found = 'SI'
	return found

#Obtiene los Na ssh para los eventos criticos
def obtenerNa(counter, severity, titulo, descripcion):
	respuesta = ' '
	descripcionLow = descripcion.lower()
	tituloLow = titulo.lower()
	if(severity.lower() == CRITICAL):
		if(counter == 'SI'):
			respuesta = 'SI'
		elif (descripcionLow.find(NORESPONSE) != -1):
			respuesta = 'SI'
		else:
			for tit in titulos:
				if(tituloLow.find(tit.lower()) != -1):
					respuesta = 'SI'
	return respuesta

# Obtiene las maquinas Ci para los eventos criticos
def obtenerCi(severity, node):
	respuesta = ' '
	if (severity.lower() == CRITICAL):
		pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
		test = pat.match(node)
		if(not test):
			respuesta = node
	return respuesta

#Obtiene la duracion del evento para los eventos criticos
def obtenerTiempo(horaInicial, horaFinal, severity):
	if(severity.lower() == CRITICAL):
		fechaIDate = datetime.strptime(formatDate(horaInicial), '%Y-%m-%dT%H:%M:%S')
		fechaFDate = datetime.strptime(formatDate(horaFinal), '%Y-%m-%dT%H:%M:%S')
		diff = fechaFDate - fechaIDate
		text = str(diff)
		return text
	else :
		return ' '

#Le da a las fechas el formato correcto para poder convertirlas a objeto tipo datetime
def formatDate(paramFecha):
	fecha = ''
	splitF = paramFecha.split('.')
	fechaFormat = splitF[0]
	fecha = fechaFormat.split(',')
	return fecha[0]

# Obtiene el sistema operativo para los eventos
def obtenerSO(objeto, ciType, aplicacion):
	encontro = False
	objetoLow = objeto.lower()
	ciTypeLow = ciType.lower()
	aplicacionLow = aplicacion.lower()
	so = aplicacion

	if(objetoLow.find(WINDOWS) != -1 or ciTypeLow.find(WINDOWS) != -1 or aplicacionLow.find(WINDOWS) != -1):
		encontro = True
		so ='WINDOWS'

	elif (encontro == False):
		for sis in sistemasOperativosSSH: 
			if(objetoLow.find(sis) != -1 or ciTypeLow.find(sis) != -1 or aplicacionLow.find(sis) != -1):
				encontro = True
				so = 'UNIX'
				break

	return so

#Obtiene los clientes de los eventos
def obtenerCliente(title):
	split = title.split('//')
	if (len(split)>1 and split[len(split)-1].find(' - ') != -1 and split[len(split)-1].find(' @ ') == -1 and split[len(split)-1].find(' CRITICAL ') == -1 and split[len(split)-1].find(' OK ') == -1):
		return split[len(split)-1].strip()
	else:
		return 'no hay'

#Obtiene la categoria de los eventos
def obtenerCategoria(descripcion, objeto, categoria):

	descripcionLow = descripcion.lower()
	objetoLow = objeto.lower()
	categoriaLow = categoria.lower()
	respuesta = ' '

	if(descripcionLow.find('disco') != -1 or descripcionLow.find('disk') != -1 or objetoLow.find('disco') != -1 or objetoLow.find('disk') != -1 or categoriaLow.find('disco') != -1 or categoriaLow.find('disk')!= -1):
		respuesta = 'Disk'
	elif(descripcionLow.find('proceso uptime') != -1 or objetoLow.find('proceso uptime') != -1 or categoriaLow.find('proceso uptime') != -1):
		respuesta = 'proceso uptime'

	elif(descripcionLow.find('memory') != -1 or descripcionLow.find('memoria') != -1 or descripcionLow.find('swap') != -1 or categoriaLow.find('memory') != -1 or categoriaLow.find('memoria') != -1 or categoriaLow.find('swap') != -1 or objetoLow.find('memory') != -1 or objetoLow.find('memoria') != -1 or objetoLow.find('swap') != -1):
		respuesta = 'Memory'

	elif(descripcionLow.find('cpu') != -1 or objetoLow.find('cpu') != -1 or categoriaLow.find('cpu')!= -1):
		respuesta = 'CPU'

	elif(descripcionLow.find('base de datos') != -1 or descripcionLow.find('database') != -1 or categoriaLow.find('base de datos') != -1 or categoriaLow.find('database') != -1 or objetoLow.find('base de datos') != -1 or objetoLow.find('database') != -1):
		respuesta = 'Memory'

	elif(descripcionLow.find('almacenamiento') != -1 or objetoLow.find('almacenamiento') != -1 or categoriaLow.find('almacenamiento')!= -1):
		respuesta = 'Almacenamiento'

	elif(descripcionLow.find('interface caida') != -1 or objetoLow.find('interface caida')!= -1 or categoriaLow.find('interface caida')!= -1):
		respuesta = 'Interface caida'

	elif(descripcionLow.find('interface index') != -1 or objetoLow.find('interface index')!= -1 or categoriaLow.find('interface index')!= -1):
		respuesta = 'Interface Index'

	elif(descripcionLow.find('firewall')!= -1 or objetoLow.find('firewall')!= -1 or categoriaLow.find('firewall')!= -1):
		respuesta =  'Firewall'

	elif(descripcionLow.find('filesystem') != -1 or objetoLow.find('filesystem') != -1 or categoriaLow.find('filesystem') != -1):
		respuesta = 'Filesystem'

	elif(descripcionLow.find('host down') != -1 or objetoLow.find('host down') != -1 or categoriaLow.find('host down') != -1):
		respuesta = 'Host down'

	elif (respuesta == ' '):
		with open('categorias.csv' , 'r') as maquina:
			reader = csv.reader(maquina, delimiter=';')
			for line in reader:
				lineLow = line[0].lower()
				
				if(categoriaLow.find(lineLow) != -1 or descripcionLow.find(lineLow) != -1 or objetoLow.find(lineLow) != -1):
					respuesta = 'Capa Media'
					break
			if (respuesta == ' '):
				respuesta = categoria

	return respuesta

#Obtiene la categoria de los eventos
def obtenerFranja6Min(timeCreated, fechaDia):
	string2 = timeCreated.split('.')
	string = string2[0].split(',')
	hora = datetime.strptime(string[0], '%Y-%m-%dT%H:%M:%S')
	horaComp = datetime.strptime(fechaDia + ' ' + '00:00:00', '%Y-%m-%d %H:%M:%S')
	franja6 = ' '
	encontro = False
	i = 0
	while i<240:
		if(horaComp <= hora and (horaComp + timedelta(minutes = 6)) > hora):
			franja6 = franjaH = str(horaComp).split(' ')[1] + ' hasta ' + str(horaComp + timedelta(minutes = 5, seconds = 59)).split(' ')[1]
			i = 240
		else:
			horaComp = horaComp + timedelta(minutes = 6)
			i += 1
		# print (str(hora) + ' franja: ' + franjaH)
	return franja6

def main( ):
	diaD = input('ingrese el día del que se esta realizando la data (doble digito ej: 01, 15, 20)')
	mesD = input('ingrese el mes del que se esta realizando la data (doble digito ej: 01, 15, 20)')
	anoD = input('ingrese el año del que se esta realizando la data (cuatro digitos ej: 2019, 2015, 2020)')
	fechaDia = anoD + '-' + mesD + '-' + diaD

	with open ('Event-List-Export.csv', 'r') as csvRead:
		with open (diaD + mesD + anoD + '.csv', 'w') as csvWriter:
			reader = csv.reader(csvRead, delimiter=';')
			writer = csv.writer(csvWriter, delimiter=';')
			titles = ('Día', 'Hora Inicial', 'Hora Final', 'Franja Horaria', 'Variable', 'Wmi', 'net', 'Ssh', 'no identificado', 'counter', 'Na', 'Ci', 'Tiempo alarma', 'Block', 'SO', 'Incidente', 'Cliente', 'Categoria', 'Franja 6 minutos')
			rowCounter = 0
			for row in reader:
				toWrite = [ ]*46
				severity = row[0]
				title = row[10]
				assignedGroup = row[13]
				category = row[14]
				application = row[16]
				if (not row[17]):
					CIType = ' '
				else:
					CIType = row[17]
				descripcion = row[21]
				nodeHint = row[27]
				objeto = row[28]
				timeCreated = row[40]
				timeEnd = row[42]
				net = ''
				wmi = ''
				dia = 0
				if (not row[26]):
					node = ' '
				else:
					node = row[26]
				counter = ''
				for col in row:
					toWrite.append(col)
				if (rowCounter != 0):
					dia = obtenerDia(timeCreated)
					toWrite.append(str(dia))
					toWrite.append(str(obtenerHoraInicial(timeCreated)))
					toWrite.append(str(obtenerHoraFinal(timeEnd)))
					if (int(dia) == int(diaD)):
						franjaHoraria = obtenerFranjaHoraria(timeCreated, fechaDia)
					else:
						franjaHoraria = ''
					toWrite.append(franjaHoraria)
					toWrite.append('')
					net = obtenerNet(severity, nodeHint, title, descripcion)
					wmi = obtenerWmi(severity, objeto, title, descripcion, CIType, net)
					ssh = obtenerSsh(severity, objeto, title, descripcion, CIType, net, wmi)
					toWrite.append(wmi)
					toWrite.append(net)
					toWrite.append(ssh)
					toWrite.append(obtenerNoIden(severity, title, objeto, CIType, descripcion))
					counter = (obtenerCounter(severity, title))
					toWrite.append(counter)
					toWrite.append(obtenerNa(counter, severity, title, descripcion))
					toWrite.append(obtenerCi(severity, node))
					toWrite.append(obtenerTiempo(timeCreated, timeEnd, severity))
					toWrite.append('')
					toWrite.append(obtenerSO(objeto, CIType, application))
					toWrite.append('')
					toWrite.append(obtenerCliente(title))
					toWrite.append(obtenerCategoria(descripcion, objeto, category))
					if (int(dia) == int(diaD)):
						franjaMin = obtenerFranja6Min(timeCreated, fechaDia)
					else:
						franjaMin = ''
					toWrite.append(franjaMin)
				else:
					for titleIn in titles:
						toWrite.append(titleIn)
						rowCounter = 1
				writer.writerow(toWrite)
main()
