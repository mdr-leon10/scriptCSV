import csv
cont = 0
with open ('ConsolidadoFebrero.csv', 'r') as data:
	with open ('export.csv', 'r') as sm:
		with open ('cruzado.csv', 'w') as cruzado:
			reader = csv.reader(data, delimiter=';')
			reader1 = csv.reader(sm, delimiter=';')
			writer = csv.writer(cruzado, delimiter=';')
			for row in reader:
				if(cont != 0):
					externalID =row[23]
					grupoAsig ='N/A '
					ci = 'N/A '
					if('IM' in externalID):
						for row1 in reader1:
							if (externalID in row1[0] or row[0] in externalID):
								grupoAsig = row1[1]
								ci = row1[2]
								# print(row[2])
								row.append(grupoAsig)
								row.append(ci)
								writer.writerow(row)
								break
							# row.append(grupoAsig)
							# row.append(ci)
							# writer.writerow(row)
				else:
					row.append('grupo de Asignación')
					row.append('El CI esta funcional')
					writer.writerow(row)
					cont += 1
				
				sm.seek(0)
				