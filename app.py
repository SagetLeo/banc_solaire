from flask import Flask, Response, render_template
import json
import time
import mysql.connector
import datetime
from flask import request




app = Flask(__name__)

def get_mesure_data(sensor_name): #PVbusvoltage	
	conn= mysql.connector.connect(host="localhost",user="root",password="RASPBERRY",database="projettut")
	cursor = conn.cursor()

	# recuperation du tuple (mesure, date) dans la db

	query = "SELECT valeur,time FROM bancsolaire WHERE nom_capteur = %s"
	data = (str(sensor_name),)
	cursor.execute(query,data)
	datarec = cursor.fetchall()

	listdata=[]
	for i in range(0,len(datarec)):
		date = datarec[i][1]
		value = datarec[i][0]
		string = "{y: "+str(value)+", x: "+str(date)+"}"
		print(string)
		listdata.append(string)
	listdata = str(listdata).replace("'","")
	cursor.close()
	conn.close()
	return listdata


@app.teardown_appcontext
def close_connection(exception):
	try:
		conn.close()
	except:
		print("...! Warning [conn.close()]...")
	print(".... ok")
	try:
		cursor.close()
	except:
		print("...! Warning [cursor.close()]...")
	print(".... ok")


#PVbusV PVshtV PVA PVloadV PVpower 

#PVbusV = str(get_mesure_data(PVbusV)),PVshtV = str(get_mesure_data(PVshtV)),PVA = str(get_mesure_data(PVA)),PVloadV = str(get_mesure_data(PVloadV)),PVpower  = str(get_mesure_data(PVpower )),

#BATbusV BATshtV BATA BATloadV BATpower 

#BATbusV = str(get_mesure_data(BATbusV)),BATshtV = str(get_mesure_data(BATshtV)),BATA = str(get_mesure_data(BATA)),BATloadV = str(get_mesure_data(BATloadV)),BATpower = str(get_mesure_data(BATpower)),

#LOAD1busV LOAD1shtV LOAD1A LOAD1loadV LOAD1power

#LOAD1busV = str(get_mesure_data(LOAD1busV)),LOAD1shtV = str(get_mesure_data(LOAD1shtV)),LOAD1A = str(get_mesure_data(LOAD1A)),LOAD1loadV = str(get_mesure_data(LOAD1loadV)),LOAD1power = str(get_mesure_data(LOAD1power)),

#LOAD2busV LOAD2shtV LOAD2A LOAD2loadV LOAD2power

#LOAD2busV = str(get_mesure_data(LOAD2busV)),LOAD2shtV = str(get_mesure_data(LOAD2shtV)),LOAD2A = str(get_mesure_data(LOAD2A)),LOAD2loadV = str(get_mesure_data(LOAD2loadV)),LOAD2power = str(get_mesure_data(LOAD2power))


#PVbusV PVshtV PVA PVloadV PVpower 
#BATbusV BATshtV BATA BATloadV BATpower 
#LOAD1busV LOAD1shtV LOAD1A LOAD1loadV LOAD1power
#LOAD2busV LOAD2shtV LOAD2A LOAD2loadV LOAD2power


@app.route('/', methods=['GET'])
def get_index():

	PVbusV = "PVbusV"
	PVshtV = "PVshtV"
	PVA = "PVA"
	PVloadV = "PVloadV"
	PVpower = "PVpower"
	
	BATbusV = "BATbusV"
	BATshtV = "BATshtV"
	BATA = "BATA"
	BATloadV = "BATloadV"
	BATpower = "BATpower"
	
	LOAD1busV = "LOAD1busV"
	LOAD1shtV = "LOAD1shtV"
	LOAD1A = "LOAD1A"
	LOAD1loadV = "LOAD1loadV"
	LOAD1power = "LOAD1power"
	
	LOAD2busV = "LOAD2busV"
	LOAD2shtV = "LOAD2shtV"
	LOAD2A = "LOAD2A"
	LOAD2loadV = "LOAD2loadV"
	LOAD2power = "LOAD2power"


	return render_template('index.html',PVbusV = str(get_mesure_data(PVbusV)),PVshtV = str(get_mesure_data(PVshtV)),PVA = str(get_mesure_data(PVA)),PVloadV = str(get_mesure_data(PVloadV)),PVpower  = str(get_mesure_data(PVpower )),BATbusV = str(get_mesure_data(BATbusV)),BATshtV = str(get_mesure_data(BATshtV)),BATA = str(get_mesure_data(BATA)),BATloadV = str(get_mesure_data(BATloadV)),BATpower = str(get_mesure_data(BATpower)),LOAD1busV = str(get_mesure_data(LOAD1busV)),LOAD1shtV = str(get_mesure_data(LOAD1shtV)),LOAD1A = str(get_mesure_data(LOAD1A)),LOAD1loadV = str(get_mesure_data(LOAD1loadV)),LOAD1power = str(get_mesure_data(LOAD1power)),LOAD2busV = str(get_mesure_data(LOAD2busV)),LOAD2shtV = str(get_mesure_data(LOAD2shtV)),LOAD2A = str(get_mesure_data(LOAD2A)),LOAD2loadV = str(get_mesure_data(LOAD2loadV)),LOAD2power = str(get_mesure_data(LOAD2power)))




@app.route('/mesures/<capteur>', methods=['GET'])
def get_mesure_capteur(capteur):


	if (capteur == "PV"):
		busV = "PVbusV"
		shtV = "PVshtV"
		A = "PVA"
		loadV = "PVloadV"
		power = "PVpower"

	if (capteur == "BAT"):	
		busV = "BATbusV"
		shtV = "BATshtV"
		A = "BATA"
		loadV = "BATloadV"
		power = "BATpower"

	if (capteur == "LOADmain"):
		busV = "LOAD1busV"
		shtV = "LOAD1shtV"
		A = "LOAD1A"
		loadV = "LOAD1loadV"
		power = "LOAD1power"
	
	if (capteur == "LOADdevice"):
		busV = "LOAD2busV"
		shtV = "LOAD2shtV"
		A = "LOAD2A"
		loadV = "LOAD2loadV"
		power = "LOAD2power"

	busV = str(get_mesure_data(busV))
	shtV = str(get_mesure_data(shtV))
	A = str(get_mesure_data(A))
	loadV = str(get_mesure_data(loadV))
	power  = str(get_mesure_data(power ))


	return render_template('mesure_capteur.html',busV=busV,shtV=shtV,A=A,loadV=loadV,power=power,capteur=capteur)
	
	

@app.route('/power', methods=['GET'])
def get_mesure_power():

	PVpower = str(get_mesure_data("PVpower"))
	BATpower = str(get_mesure_data("BATpower"))
	LOAD1power = str(get_mesure_data("LOAD1power"))
	LOAD2power  = str(get_mesure_data("LOAD2power"))


	return render_template('mesure_power.html',PVpower=PVpower,BATpower=BATpower,LOAD1power=LOAD1power,LOAD2power=LOAD2power)
	
	
@app.route('/pv_bat', methods=['GET'])
def get_mesure_pv_bat():

	PVpower = str(get_mesure_data("PVpower"))
	BATpower = str(get_mesure_data("BATpower"))
	PVA = str(get_mesure_data("PVA"))
	BATA  = str(get_mesure_data("BATA"))


	return render_template('mesure_pvbat.html',PVpower=PVpower,BATpower=BATpower,PVA=PVA,BATA=BATA)

	
@app.route('/test', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
	val = request.args.get('val')
	return render_template('test.html',username = username, password = password, val = val)


#@app.route('/mesures', methods=['GET'])
#def get_mesure_json():

#	return_array = []
	
#	conn= mysql.connector.connect(host="localhost",user="root",password="RASPBERRY",database="projettut")
#	cursor = conn.cursor()
	
#	# recuperation du tuple (mesure, date) dans la db
#	cursor.execute("""SELECT valeur,time FROM mesures WHERE id_capteur = 5""") # capteur humidite mesure humidite
#	rows = cursor.fetchall()

#	cursor.close()
#	conn.close()

#	return render_template('index_lines2.html', data = data_format_wrong)
	

if __name__ == '__main__':
	app.debug=True
	app.run()













