from datetime import datetime
from datetime import datetime
import csv

cont = 0

def obtenerDuracion(fechaHoraI, fechaHoraF):
	fechaIDate = datetime.strptime(formatDate(fechaHoraI), '%d/%m/%Y %I:%M:%S %p')
	fechaFDate = datetime.strptime(formatDate(fechaHoraF), '%d/%m/%Y %I:%M:%S %p')

def formatDate(paramFecha):
	fecha = ''
	splitF = paramFecha.split(' ')
	fecha = splitF[0] + ' ' + splitF[2]

	if(splitF[3] == 'a.'):
		fecha = fecha + ' ' + 'AM'
	elif (splitF[3] == 'p.'):
		fecha = fecha + ' ' + 'PM'
	return fecha

def esPrimium(cliente):
	with open ('clientesPremium.csv', 'r') as clientes:
		readerClientes = csv.reader(clientes, delimiter=';')
		for row in readerClientes:
			csv = row[0]
			titulo = cliente
			if(titulo.find(csv.lower()) != -1):
				return 'SI'
			else
				return  ' '


with open ('prueba.csv', 'r') as dataContainer:
	with open ('exportsemicolon.csv', 'w') as dataProceser:
		reader = csv.reader(dataContainer, delimiter=';')
		writer = csv.writer(dataProceser, delimiter= ';')
		cont = 0
		for row in reader:
			toWrite []*25
			idIncidente = row[0]
			estado = row[1]
			prioridad = row[2]
			estadoAlerta = row[3]
			ciAfectado = row[4]
			afectadoPrincipal = row[5]
			titulo = row[6]
			creadoEventoModelo = row[7]
			reasignacion = row[8]
			origen = row[9]
			categoria = row[10]
			descripcion = row[11]
			fechahoraAct = row[12]
			fechaHoraApert = row[14]
			grupoAsignacion = row[15]
			incidenteImportante = row[16]
			compania = row[17]
			esPremium = esPremium(compania)
				esPremium = 'es Premium?'
			ciOperativo = row[18]
			Asignado = row[19]
			fechaHoraRes = row[20]
			tiempoEvento = obtenerDuracion(fechaHoraApert, fechaHoraRes)
			idInteraccion = row[21]
			incidente = row[22]
			solucion = row[23]

			if(cont != 0) :	
				toWrite = [idIncidente, estado, prioridad, estadoAlerta, ciAfectado, afectadoPrincipal, titulo, creadoEventoModelo, reasignacion, origen, categoria, descripcion, fechahoraAct, fechaHoraApert, grupoAsignacion, incidenteImportante, compania, esPremium, ciOperativo, Asignado, fechaHoraRes, tiempoEvento, idInteraccion, incidente, solución
			else:
				toWrite = [idIncidente, estado, prioridad, estadoAlerta, ciAfectado, afectadoPrincipal, titulo, creadoEventoModelo, reasignacion, origen, categoria, descripcion, fechahoraAct, fechaHoraApert, grupoAsignacion, incidenteImportante, compania, 'Es premium?', ciOperativo, Asignado, fechaHoraRes, 'Duración del evento', idInteraccion, incidente, solución]
				cont = 1