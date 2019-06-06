from flask import Flask, request, make_response, jsonify
app = flask(__name__)

@app.route('/', methods=['POST'])
def clasificar():
	req = req.get_jason(silent = True, force=True)
	try:
		action = req.get('queryResult').get('action')
	except AttributeError:
		return 'json error'

	if action == 'cedula':
		res = 'Hola (Nombre de la Persona)'
	elif action == 'nit':
		res = 'Que solicitud quieres crear para (Nombre de la empresa)'
	elif action == 'servicio':
		res = 'Por favor ingresa la descripcion de tu problema con el servicios'