import csv 

CRITICAL = 'Critical'
WINDOWS = 'Windows'
NORESPONSE = 'No response from remote host'
titulos = ['status not found', 'correlacion', 'n/a']
encabezado = [ 'Severity', 'Priority', 'Correlation', 'Annotations', 'Instructions', 'Automatic Action', 'User Action', 'Duplicate Count', 'Lifecycle State', 'Time Received (America/Bogota)', 'Title', 'Related CI', 'Assigned User', 'Assigned Group', 'Category', 'Anotacion', 'Application', 'CI Type', 'Company', 'Control Transferred', 'Customer', 'Description', 'Event Type Indicator', 'External ID', 'ID', 'Manager', 'Node', 'Node Hint', 'Object', 'Originating server', 'Owned in OM', 'Received in Downtime', 'Region', 'Related CI Hint', 'Sending Server', 'Solution', 'Source CI', 'Source CI Hint', 'Subcategory', 'Time Changed', 'Time created (America/Bogota)', 'Time First Received (America/Bogota)', 'Time Lifecycle Changed(America/Bogota)', 'Type', 'Cma1', 'Día', 'Hora Inicial', 'Hora Final', 'Franja Horaria', 'Variable', 'wmi', 'net', 'ssh', 'no iden', 'counter', 'Na', 'Ci', 'Tiempo Alarma', 'Black', 'SO', 'incidente', 'Cliente', 'Categoria', 'Franja 6 minutos']
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
def obtenerFranjaHoraria(horaInicial, obtenerHoraFinal):
	return 4

#LLena la casilla variable
def obtenerVariable():
	return ''

#Obtiene las maquinas wmi para los eventos criticos
def obtenerWmi(severity, object, titulo, descripcion, ciType, net):
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
	return 6

#Obtiene las maquinas ssh para los eventos criticos
def obtenerSsh(severity, object, titulo, descripcion, ciType, net, wmi):
	foundMatch = false 
	for SO in sistemasOperativosSSH
		if (severity == CRITICAL and object.find(SO) != -1 and net == '' and wmi == '' ):

			if (descripcion.find(NORESPONSE) != -1):
				foundMatch = true
			else: 
				for tit in titulos:  
					if (titulo.find(tit) != -1):
						foundMatch = true
		else if if (severity == CRITICAL and object.find(SO) == -1 and ciType.find(SO) != -1)
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

def obtenerBlack():
	return ''

#Obtiene el sistema operativo para los eventos
def obtenerSO(object, ciType, aplicacion):
	return 13

def obtenerIncidente():
	return ''

#Obtiene los clientes de los eventos
def obtenerCliente(titulo):
	return 14

#Obtiene la categoria de los eventos
def obtenerCategoria(titulo, descripcion, object):
	return 15

# función principal del script: lee el archivo, escribe el archivo, llama al resto de funciones.
def main():
    open with ('dd-mm-aaaa.csv', 'w') as csv:
    	csv.writerow(encabezado)
    	open with ('prueba.csv', 'r') as data:
    		contador = 0
    		for row in data:
    			if (contador != 0):
    				for i in range(0, 44) :
    					dataRow.append(i)
    					contador+=1 
    			else:
    				contador +=1
