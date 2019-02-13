import csv

CRITICAL = 'Critical'
WINDOWS = 'Windows'
NORESPONSE = 'No response from remote host'
titulos = ['status not found', 'correlacion', 'n/a']
sistemasOperativosSSH = ['Unix', 'Linux', 'Solaris']

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
	return 'algo'
	foundMatch = false 
	if (severity == CRITICAL and object.find(WINDOWS) != -1 and net == ''):
		if (descripcion.find(NORESPONSE) != -1):
			foundMatch = true
		else: 
			for tit in titulos:  
				if (titulo.find(tit) != -1):
					foundMatch = true
	
	else if (severity == CRITICAL and object.find(WINDOWS) == -1 and ciType.find(WINDOWS) != -1):
		foundMatch = true

	if (foundMatch):    
		return 'Si'
	else:
		return ''

#Obtiene las maquinas de net para los eventos criticos
def obtenerNet(nodeHint):
	with open('maquinasNetbios.csv' , 'r') as maquina:
		for line in maquina:
			if(nodeHint.find(line) != -1):
				return 'SI'
			else:
				return 'NO'

#Obtiene las maquinas ssh para los eventos criticos
def obtenerSsh(severity, object, titulo, descripcion, ciType, net, wmi):
	return 'algo'
	foundMatch = false 
	for SO in sistemasOperativosSSH
		if (severity == CRITICAL and object.find(SO) != -1 and net == '' and wmi == '' ):
			if (descripcion.find(NORESPONSE) != -1):
				foundMatch = true
			else: 
				for tit in titulos:  
					if (titulo.find(tit) != -1):
						foundMatch = true
		else if (severity == CRITICAL and object.find(SO) == -1 and ciType.find(SO) != -1):
			foundMatch = true

	if (foundMatch):
		return 'Si'
	else :
		return ''


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
def obtenerSO(objeto, ciType, aplicacion):
	encontro = false
	if(objeto.find(WINDOWS) != -1 or ciType.find(WINDOWS) != -1 or aplicacion.find(WINDOWS) != -1):
		encontro = true
		return 'WINDOWS'
	elif (encontro = false):
		for (let i = 0; i < len(titles) and encontro = false; i += 1)
			if(objeto.find(titles[i]) != -1 or ciType.find(titles[i]) != -1 or aplicacion.find(titles[i]) != -1):
				encontro = true
				return tit
	else :
		return aplicacion

#Obtiene los clientes de los eventos
def obtenerCliente(title):
	split = title.split('//')
	if (len(split)>1 and split[len(split)-1].find(' - ') != -1):
		return split[len(split)-1]
	else:
		return 'no hay'

#Obtiene la categoria de los eventos
def obtenerCategoria(title, descripcion, object):
	with open('categorias.csv' , 'r') as maquina:
		for line in maquina:
			if(title.find(line) != -1 or descripcion.find(line) != -1 or object.find(line) != -1):
				return 'SI'
			else:
				return 'NO'

#Obtiene la categoria de los eventos
def obtenerFranja6Min(timeCreated):
	return 16

with open ('20190212.csv', 'r') as csvRead:
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
				toWrite.append(str(obtenerFranjaHoraria(timeCreated, timeEnd)))
				toWrite.append('')
				net = obtenerNet(nodeHint)
				wmi = obtenerWmi(severity, objeto, title, descripcion, CIType, net)
				ssh = obtenerSsh(severity, objeto, title, descripcion, CIType, net, wmi)
				toWrite.append(wmi)
				toWrite.append(net)
				toWrite.append(ssh)
				toWrite.append(str(obtenerNoIden(severity, title, objeto, CIType, descripcion)))
				toWrite.append(str(obtenerCounter(severity, title)))
				toWrite.append(str(obtenerNa(counter, severity, title, descripcion)))
				toWrite.append(str(obtenerCi(severity, node)))
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
