import csv

#Obtiene el día del evento a partir de la hora dada por parametro
def obtenerDia(horaInical):
    return 1

#Obtiene la hora inicial del evento a partir de la hora dada por parametro
def obtenerHoraInicial(horaInicial):
    return 2

#Obtiene la hora final del evento a partir de la hora dada por parametro
def obtenerHoraFinal(horaFinal):
    return 3

#Obtiene la franja horaria a la que pertenece el evento a partir de la hora dada por paráametro
def obtenerFranjaHoraria(horaInicial, horaFinal):
    return 4

#Obtiene las maquinas wmi para los eventos criticos
def obtenerWmi(severity, object, titulo, descripcion, ciType, net):
#	foundMatch = false 
#	if (severity == CRITICAL and object.find(WINDOWS) != -1 and net == ''):
#		if (descripcion.find(NORESPONSE) != -1):
#			foundMatch = true
#		else: 
#			for tit in titulos:  
#				if (titulo.find(tit) != -1):
#					foundMatch = true
#	
#	else if (severity == CRITICAL and object.find(WINDOWS) == -1 and ciType.find(WINDOWS) != -1):
#		foundMatch = true

#	if (foundMatch):    
#		return 'Si'
#	else:
#		return ''
	return 'algo'

#Obtiene las maquinas de net para los eventos criticos
def obtenerNet(nodeHint):
    return 6

#Obtiene las maquinas ssh para los eventos criticos
def obtenerSsh(severity, object, titulo, descripcion, ciType, net, wmi):
#	foundMatch = false 
#	for SO in sistemasOperativosSSH
#		if (severity == CRITICAL and object.find(SO) != -1 and net == '' and wmi == '' ):
#			if (descripcion.find(NORESPONSE) != -1):
#				foundMatch = true
#			else: 
#				for tit in titulos:  
#					if (titulo.find(tit) != -1):
#						foundMatch = true
#		else if (severity == CRITICAL and object.find(SO) == -1 and ciType.find(SO) != -1):
#			foundMatch = true
#
#	if (foundMatch):
#		return 'Si'
#	else :
#		return ''
	return 'algo'

#Obtiene las maquinas no identificadas para los eventos criticos
def obtenerNoIden(severity, titulo, object, ciType, descripcion):
    return 8
#Obtiene los counters para los eventos criticos
def obtenerCounter(severity, titulo):
    return 9
#Obtiene los Na ssh para los eventos criticos
def obtenerNa(counter, severity, titulo, descripcion):
    return 10

#Obtiene las maquinas Ci para los eventos criticos
def obtenerCi(severity, node):
    return 11

#Obtiene la duracion del evento para los eventos criticos
def obtenerTiempo(horaInicial, horaFinal):
    return 12

#Obtiene el sistema operativo para los eventos
def obtenerSO(object, ciType, aplicacion):
    return 13

#Obtiene los clientes de los eventos
def obtenerCliente(title):
	split = title.split('//')
	if (len(split)>1 and split[len(split)-1].find(' - ') != -1):
		return split[len(split)-1]
	else:
		return 'no hay'

#Obtiene la categoria de los eventos
def obtenerCategoria(titulo, descripcion, object):
    return 15

#Obtiene la categoria de los eventos
def obtenerFranja6Min(timeCreated):
    return 16

#Abre el archivo que se va a leer
with open ('20190212.csv', 'r') as csvRead:
	
	#Abre el archivo que se va a escribir
	with open ('ddmmaaa.csv', 'w') as csvWriter:
		
		#Inicializa el lector
		reader = csv.reader(csvRead, delimiter=';')
		
		#Inicializa el escritor
		writer = csv.writer(csvWriter, delimiter=';')
		
		#Titulos de las columnas
		titles = ('Día', 'Hora Inicial', 'Hora Final', 'Franja Horaria', 'Variable', 'Wmi', 'net', 'Ssh', 'no identificado', 'counter', 'Na', 'Ci', 'Tiempo', 'Block', 'SO', 'Incidente', 'Cliente', 'Categoria', 'Franja 6 minutos')
		
		#Contador de columnas
		rowCounter = 0
		
		# Ciclo que recorre cada fila del csv
		for row in reader:

			#Lista donde se almacena la información que se va a escribir
			toWrite = [ ]*46

			#Variables requeridas para realizar el análisis de la información. La información que se extrae se encuentra en el archivo original.
			severity = row[0]
			title = row[10]
			application = row[16]
			CIType = row[17]
			descripcion = row[21]
			nodeHint = row[27]
			objeto = row[28]
			timeCreated = row[40]
			timeEnd = row[42]
			
			#Variables requeridas para realizar el análisis de la información. La información qes de métodos que se ejecutan anteriormente.
			net = ''
			wmi = ''
			node = ''
			counter = ''

			#Recorre cada columna en la fila y guarda la data necesaria.
			for col in row:
				toWrite.append(col)
				if (rowCounter != 0):
					toWrite.append(str(obtenerDia(timeCreated)))
					toWrite.append(str(obtenerHoraInicial(timeCreated)))
					toWrite.append(str(obtenerHoraFinal(timeEnd)))
					toWrite.append(str(obtenerFranjaHoraria(timeCreated, timeEnd)))
					toWrite.append('')
					net = obtenerNet(nodeHint)
					wmi = obtenerWmi(severity, objeto, title, descripcion, CIType, net)
					toWrite.append(wmi)
					toWrite.append(net)
					toWrite.append(obtenerSsh(severity, objeto, title, descripcion, CIType, net, wmi))
					toWrite.append(obtenerNoIden(severity, title, objeto, CIType, descripcion))
					toWrite.append(obtenerCounter(severity, title))
					toWrite.append(obtenerNa(counter, severity, title, descripcion))
					toWrite.append(obtenerCi(severity, node))
					toWrite.append(str(obtenerTiempo(timeCreated, timeEnd)))
					toWrite.append('')
					toWrite.append(str(obtenerSO(objeto, CIType, application)))
					toWrite.append('')
					toWrite.append(str(obtenerCliente(title)))
					toWrite.append(str(obtenerCategoria(title, descripcion, objeto)))
					toWrite.append(str(obtenerFranja6Min(timeCreated)))
				else:
					for titleIn in titles:
						toWrite.append(titleIn)
						rowCounter = 1
		writer.writerow(toWrite)
