from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask import jsonify
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

############ LOG #############
import datetime 
import requests
log_microservice = "http://127.0.0.1:43000/"
@app.before_request
def before_request_func():
	args = request.args.get("key")
	if args == None:
		args = "Undefined User"
	if args == "":
		args = "Undefined User"
	
	data = {
		'date' : str(datetime.datetime.now()),
		'method' : request.method,
		'microservice' : 'rooms',
		'args' : args,
		'request' : str(request)
	}
	try:
		req = requests.post(url = log_microservice + "add", data = data) 
		if req.status_code != 200:
			print("Log service not available")
	except Exception as e:
		print("ERROR - Logging"+str(e))

def jprint(obj):
	# create a formatted string of the Python JSON object
	text = json.dumps(obj, sort_keys=True, indent=4)
	print(text)

@app.route('/rooms')
def rooms():
	message = {}
	try:
		resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces")

		if resp.status_code != 200:
			#This means something went wrong.
			message = {
				'status_code': 404,
				'message': 'Resource not found',
				'rooms': None
			}
		else:
			campus = resp.json()
			message = {
				'status_code': 200,
				'message'    : 'OK',
				'rooms' : campus
			}		
	except:
		message = {
			'status_code': 404,
			'message': 'Unable to perform API resquest to Fenix',
			'rooms': None
		}
	
	return jsonify(message)

@app.route('/rooms/<id>')
def room_location(id):
	message = {}
	try:
		resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+str(id))

		if resp.status_code != 200:
			#This means something went wrong.
			message = {
				'status_code': 404,
				'message': 'Resource not found',
				'rooms': None
			}
		else:
			pass_times = resp.json()
			
			room_local = {
				'ID'   : pass_times['id'],
				'Room'   : pass_times['name'],
				'Campus'      : pass_times['topLevelSpace']['name'],
				'Capacity'   : pass_times['capacity']['normal']
			}
			message = {
				'status_code': 200,
				'message'    : 'OK',
				'rooms' : room_local
			}		
	except:
		message = {
			'status_code': 404,
			'message': 'Unable to perform API resquest to Fenix',
			'rooms': None
		}
	return jsonify(message)


@app.route('/rooms/<id>/<day>/<mouth>/<year>')
def rooms_timetable(id, day, mouth, year):
	message = {}
	try:
		resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+str(id)+"?day="+str(day)+"/"+str(mouth)+"/"+str(year))
		if resp.status_code != 200:
			#This means something went wrong.
			message = {
				'status_code': 404,
				'message': 'Resource not found',
				'rooms': None
			}
		else:
			pass_times = resp.json()
			# All events of that week
			events = resp.json()['events']
			# Filtering by day required
			schedule = []
			for d in events:
				if d['day'] == str(day)+"/"+str(mouth)+"/"+str(year):
					slot = {
							'Course' : d['course']['name'],
							'acronym' : d['course']['acronym'],
							'period' : d['period'],
							'info' : d['info'],
							'type' : d['type']
						}
					schedule.append(slot)

			room_timetable = {
				'ID'      : pass_times['id'],
				'Room'    : pass_times['name'],
				'type'    : resp.json()['type'],
				'day'     : str(day),
				'mouth'   : str(mouth),
				'year'    : str(year),
				'schedule': schedule
			}

			message = {
				'status_code': 200,
				'message': 'OK',
				'rooms': room_timetable
			}
	except :
		message = {
			'status_code': 404,
			'message': 'Unable to perform API resquest to Fenix',
			'rooms': None
		}
	
	return jsonify(message)

if __name__ == '__main__':
	app.run(debug=True, port=40000)
 