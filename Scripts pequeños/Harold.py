from datetime import datetime
import csv

cont = 0

def obtenerDuracion(fechaHoraI, fechaHoraF):
	try:
		fechaIDate = datetime.strptime(fechaHoraI, '%d/%m/%Y %H:%M')
		fechaFDate = datetime.strptime(fechaHoraF, '%d/%m/%Y %H:%M')
		diff = fechaIDate - fechaFDate
		result = str(diff.days)
		return result
	except:
		return 'No ha sido resuelto'

def esPremium(cliente):
	result = ' '
	with open ('clientesPremium.csv', 'r') as clientes:
		readerClientes = csv.reader(clientes, delimiter=';')
		for row in readerClientes:
			arch = row[0]
			titulo = cliente.lower()
			if(titulo.find(arch.lower()) != -1):
				result = 'SI'
		return result


with open ('export.csv', 'r', errors='ignore') as dataContainer:
	with open ('exportsemicolon.csv', 'w') as dataProceser:
		reader = csv.reader(dataContainer, delimiter=';')
		writer = csv.writer(dataProceser, delimiter= ';')
		cont = 0
		for row in reader:
			toWrite = [ ]*25
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
			fechaHoraApert = row[13]
			grupoAsignacion = row[14]
			incidenteImportante = row[15]
			compania = row[16]
			esPremiumS = esPremium(compania)
			ciOperativo = row[17]
			Asignado = row[18]
			fechaHoraRes = row[19]
			tiempoEvento = obtenerDuracion(fechaHoraApert, fechaHoraRes)
			idInteraccion = row[20]
			incidente = row[21]
			solucion = row[22]

			if(cont != 0) :	
				toWrite = [idIncidente, estado, prioridad, estadoAlerta, ciAfectado, afectadoPrincipal, titulo, creadoEventoModelo, reasignacion, origen, categoria, descripcion, fechahoraAct, fechaHoraApert, grupoAsignacion, incidenteImportante, compania, esPremiumS, ciOperativo, Asignado, fechaHoraRes, tiempoEvento, idInteraccion, incidente, solucion]
			else:
				toWrite = [idIncidente, estado, prioridad, estadoAlerta, ciAfectado, afectadoPrincipal, titulo, creadoEventoModelo, reasignacion, origen, categoria, descripcion, fechahoraAct, fechaHoraApert, grupoAsignacion, incidenteImportante, compania, 'Es premium?', ciOperativo, Asignado, fechaHoraRes, 'Duracion del evento', idInteraccion, incidente, solucion]
				cont = 1
			writer.writerow(toWrite)
