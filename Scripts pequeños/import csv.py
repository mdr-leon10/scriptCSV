#!/usr/bin/env python3
import csv
cliente = ''


with open ('prueba.csv', 'r') as csvfile:
	with open ('resultadoPrueba.csv', 'w') as csvWrite:
		writer = csv.writer(csvWrite)
		prueba = csv.reader(csvfile)
		for row in prueba:
			print(str(len(row)))
			if(len(row)>= 1):
				split = row[0].split('//')
				if (len(split)>1 and split[len(split)-1].find(' - ') != -1):
					cliente = split[len(split)-1]
				else:
					cliente = 'no hay'  
			writer.writerow([cliente])
		
