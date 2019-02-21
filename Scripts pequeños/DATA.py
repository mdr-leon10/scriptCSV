import csv
from datetime import datetime

CRITICAL = 'critical'
WINDOWS = 'windows'
NORESPONSE = 'no response from remote host'
titulos = ['status not found', 'correlacion', 'n/a']
sistemasOperativosSSH = ['unix', 'linux', 'solaris']

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
# def obtenerFranjaHoraria(horaInicial):
# 	return 4

#Obtiene las maquinas wmi para los eventos criticos
def obtenerWmi(severity, objeto, titulo, descripcion, ciType, net):
	foundMatch = False
	objectLow = objeto.lower()
	descripcionLow = descripcion.lower()
	tituloLow = titulo.lower()
	ciTypeLow = ciType.lower()
	if(severity.lower() == CRITICAL): 
		if (objectLow.find(WINDOWS) != -1 and net != 'SI'):
			if (descripcionLow.find(NORESPONSE) != -1):
				foundMatch = True
			else: 
				for tit in titulos:
					if (titulo.find(tit.lower()) != -1):
						foundMatch = True
		
		elif (severity,lower() == CRITICAL and objectLow.find(WINDOWS) == -1 and ciTypeLow.find(WINDOWS) != -1):
			foundMatch = true

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
	print (nodeHintLow)
	if (severity.lower() == CRITICAL):
		with open('maquinasNetbios.csv' , 'r') as maquina:
			for line in maquina:
				if(nodeHintLow.find(line.lower()) != -1):
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
	if (severity.lower() == CRITICAL):
		foundMatch = False 
		for SO in sistemasOperativosSSH:
			if (objeto.find(SO) != -1 and net != 'SI' and wmi != 'SI' ):
				if (descripcion.find(NORESPONSE) != -1):
					foundMatch = True
					break
				else: 
					for tit in titulos:  
						if (titulo.find(tit.lower) != -1):
							foundMatch = True
							break
			elif (severity.lower() == CRITICAL and objetoLow.find(SO) == -1 and ciTypeLow.find(SO) != -1):
				foundMatch = True
				break

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

	if(ciTypeLow == ' ' and severity.lower() == CRITICAL ):
		if (descripcionLow.find(NORESPONSE) != -1):
			foundit = True 
		else:
			for tit in titulos:
				if(titulo.find(tit.lower())!= -1):
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


#Obtiene las maquinas Ci para los eventos criticos
# def obtenerCi(severity, node):
# 	if (severity == CRITICAL):
# 		if(node != ' '):
# 			return node
# 		else:
# 			return ' '
# 	else 
# 		return ' '


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
	if (len(split)>1 and split[len(split)-1].find(' - ') != -1):
		return split[len(split)-1]
	else:
		return 'no hay'

#Obtiene la categoria de los eventos
# def obtenerCategoria(title, descripcion, objeto):
# 	with open('categorias.csv' , 'r') as maquina:
# 		for line in maquina:
# 			if(title.find(line) != -1 or descripcion.find(line) != -1 or objeto.find(line) != -1):
# 				return 'SI'
# 			else:
# 				return ' '

#Obtiene la categoria de los eventos
# def obtenerFranja6Min(timeCreated):
# 	return 16


with open ('20190219.csv', 'r') as csvRead:
	with open ('ddmmaaa.csv', 'w') as csvWriter:
		reader = csv.reader(csvRead, delimiter=';')
		writer = csv.writer(csvWriter, delimiter=';')
		titles = ('Día', 'Hora Inicial', 'Hora Final', 'Franja Horaria', 'Variable', 'Wmi', 'net', 'Ssh', 'no identificado', 'counter', 'Na', 'Ci', 'Tiempo', 'Block', 'SO', 'Incidente', 'Cliente', 'Categoria', 'Franja 6 minutos')
		rowCounter = 0
		for row in reader:
			toWrite = [ ]*46
			severity = row[0]
			title = row[10]
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
			node = ''
			counter = ''
			for col in row:
				toWrite.append(col)
			if (rowCounter != 0):
				toWrite.append(str(obtenerDia(timeCreated)))
				toWrite.append(str(obtenerHoraInicial(timeCreated)))
				toWrite.append(str(obtenerHoraFinal(timeEnd)))
				toWrite.append('franja horaria')#str(obtenerFranjaHoraria(timeCreated, timeEnd)))
				toWrite.append('')
				net = obtenerNet(severity, nodeHint, title, descripcion)
				# wmi = obtenerWmi(severity, objeto, title, descripcion, CIType, net)
				# ssh = obtenerSsh(severity, objeto, title, descripcion, CIType, net, wmi)
				toWrite.append('wmi')#wmi)
				toWrite.append(net)
				toWrite.append('ssh')#ssh)
				toWrite.append('no iden')#str(obtenerNoIden(severity, title, objeto, CIType, descripcion)))
				counter = (obtenerCounter(severity, title))
				toWrite.append(counter)
				toWrite.append(obtenerNa(counter, severity, title, descripcion))
				toWrite.append('Ci')#obtenerCi(severity, node))
				toWrite.append(obtenerTiempo(timeCreated, timeEnd, severity))
				toWrite.append('')
				toWrite.append(obtenerSO(objeto, CIType, application))
				toWrite.append('')
				toWrite.append(obtenerCliente(title))
				toWrite.append('categoria')#obtenerCategoria(title, descripcion, objeto))
				toWrite.append('6 min')#obtenerFranja6Min(timeCreated))
			else:
				for titleIn in titles:
					toWrite.append(titleIn)
					rowCounter = 1
			writer.writerow(toWrite)
