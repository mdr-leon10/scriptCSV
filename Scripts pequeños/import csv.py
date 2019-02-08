import csv
cliente = ''

with open ('prueba.csv', 'rb') as csvfile:
	with open ('resultadoPrueba.csv', 'w') as csvWrite:
		writer = csv.writer(csvWrite)
		prueba = csv.reader(csvfile)
		for row in prueba:
			split = row[0].split('//')
			if (split[len(split)-1].find(' - ') != -1):
				cliente = str(split[len(split)-1])
			else:
				cliente = '\n' 
			writer.writerow([cliente])

		
