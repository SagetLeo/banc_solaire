import os                   # portable way of using operating system dependent functionality
import sys                  # provides access to some variables used or maintained by the interpreter
import time                 # provides various time-related functions
import fcntl                # performs file control and I/O control on file descriptors
import serial               # encapsulates the access for the serial port
import mysql.connector 		# for bd gestion
import datetime				# for unix to human date conversion

 
 
 
 
 
 
 
 
 
 
 
if __name__ == '__main__':
	serial = serial.Serial()
	serial.port = '/dev/ttyUSB0'
	serial.baudrate = 9600
	serial.timeout = 1
	serial.writeTimeout = 1
	serial.open()
	
	# make stdin a non-blocking file
	fcntl.fcntl(sys.stdin, fcntl.F_SETFL, os.O_NONBLOCK)
	
	# post startup message to other XBee's and at stdout
	serial.writelines("RPi #1 is up and running.\r\n")
	print "RPi #1 is up and running."
	
	#maximum de trame a recevoir
	max = 500000
	
	print "Entering loop to read and print messages (Ctrl-C to abort)..."
	
	list=[]
	newlist=[]
	for t in range(0,max):
		#try:	
		# read a line from XBee and convert it from b'xxx\r\n' to xxx and print at stdout
		line = serial.readline().decode('utf-8')
		print(line)
		if (line != ""):
			if (line[0]=='!'):
				print("\n")
				print(line)
				
				# formatage des trames
				try:
						
					liste_info = line.split(';')
					
					liste_date = liste_info[0].split('=')
					date = liste_date[1].split('*')
					heure=date[0].split(':')[0]
					min=date[0].split(':')[1]
					sec=date[0].split(':')[2]
					jour=date[1].split('/')[0]
					mois=date[1].split('/')[1]
					annee=date[1].split('/')[2]
					
					
					infoPV = liste_info[1].split('=')
					infoBAT = liste_info[2].split('=')
					infoLOAD1 = liste_info[3].split('=')
					infoLOAD2 = liste_info[4].split('=')
					
					PVbusV = infoPV[1].split(':')[0]
					PVshtV = infoPV[1].split(':')[1]
					PVA = infoPV[1].split(':')[2]
					PVloadV = str(float(PVbusV) + (float(PVshtV) / 1000))
					PVpower = str(float(PVA) * float(PVloadV))
					
					BATbusV = infoBAT[1].split(':')[0]
					BATshtV = infoBAT[1].split(':')[1]
					BATA = infoBAT[1].split(':')[2]
					BATloadV = str(float(BATbusV) + (float(BATshtV) / 1000))
					BATpower = str(float(BATA) * float(BATloadV))
					
					LOAD1busV = infoLOAD1[1].split(':')[0]
					LOAD1shtV = infoLOAD1[1].split(':')[1]
					LOAD1A = infoLOAD1[1].split(':')[2]
					LOAD1loadV = str(float(LOAD1busV) + (float(LOAD1shtV) / 1000))
					LOAD1power = str(float(LOAD1A) * float(LOAD1loadV))
					
					LOAD2busV = infoLOAD2[1].split(':')[0]
					LOAD2shtV = infoLOAD2[1].split(':')[1]
					LOAD2A = infoLOAD2[1].split(':')[2]
					LOAD2loadV = str(float(LOAD2busV) + (float(LOAD2shtV) / 1000))
					LOAD2power = str(float(LOAD2A) * float(LOAD2loadV))
					
	
					dateinfo =str(date[0]+"*"+date[1])
					#print(dateinfo)
					date_time = time.mktime(datetime.datetime.strptime(dateinfo, "%H:%M:%S*%d/%m/%y").timetuple())
					#print(dateinfo)
					#print(mois)
					date = str(int(heure)+2)+":"+min+":"+sec+" "+jour+"/"+mois+"/"+annee
					print("\n"+liste_date[0][1:]+" : "+date+"\n")
					print(infoPV[0]+" : 	busvoltage = "+PVbusV+" V,	shuntvoltage = "+PVshtV+ " mV,  current_mA = "+PVA+" mA,  loadvoltage = "+PVloadV+" V,  power = "+PVpower+" mW\n")
					print(infoBAT[0]+" : 	busvoltage = "+BATbusV+" V,	shuntvoltage = "+BATshtV+ " mV,  current_mA = "+BATA+" mA,  loadvoltage = "+BATloadV+" V,  power = "+BATpower+" mW\n")
					print(infoLOAD1[0]+" :	busvoltage = "+LOAD1busV+" V,	shuntvoltage = "+LOAD1shtV+ " mV,  current_mA = "+LOAD1A+" mA,  loadvoltage = "+LOAD1loadV+" V,  power = "+LOAD1power+" mW\n")
					print(infoLOAD2[0]+" :	busvoltage = "+LOAD2busV+" V,	shuntvoltage = "+LOAD2shtV+ " mV,  current_mA = "+LOAD2A+" mA,  loadvoltage = "+LOAD2loadV+" V,  power = "+LOAD2power+" mW\n")
					
					conn= mysql.connector.connect(host="localhost",user="root",password="RASPBERRY",database="projettut")
					cursor = conn.cursor()
	
					query = "INSERT INTO bancsolaire(nom_capteur,valeur,time) " \
					"VALUES(%s, %s, %s)"
	
					data = ('PVbusV',float(PVbusV),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					data = ('PVshtV',float(PVshtV),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					data = ('PVA',float(PVA),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					data = ('PVloadV',float(PVloadV),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					data = ('PVpower',float(PVpower),str(date_time))
					cursor.execute(query,data)
					conn.commit()
	
					data = ('BATbusV',float(BATbusV),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					data = ('BATshtV',float(BATshtV),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					data = ('BATA',float(BATA),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					data = ('BATloadV',float(BATloadV),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					data = ('BATpower',float(BATpower),str(date_time))
					cursor.execute(query,data)
					conn.commit()
	
					data = ('LOAD1busV',float(LOAD1busV),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					data = ('LOAD1shtV',float(LOAD1shtV),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					data = ('LOAD1A',float(LOAD1A),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					data = ('LOAD1loadV',float(LOAD1loadV),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					data = ('LOAD1power',float(LOAD1power),str(date_time))
					cursor.execute(query,data)
					conn.commit()
	
					data = ('LOAD2busV',float(LOAD2busV),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					data = ('LOAD2shtV',float(LOAD2shtV),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					data = ('LOAD2A',float(LOAD2A),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					data = ('LOAD2loadV',float(LOAD2loadV),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					data = ('LOAD2power',float(LOAD2power),str(date_time))
					cursor.execute(query,data)
					conn.commit()
					cursor.close()
					conn.close()

				except:
					print("trame error \n\n")
	
	
		# read data from the keyboard (i.e. stdin) and send via the XBee modem
	
		try:
			line = sys.stdin.readline()
			#serial.writelines(line)
		except IOError:
			# timer ??? semble important pour le fonctionnement
			time.sleep(0.1)
			continue
	
	
	serial.writelines("""RPi #1 is going down.\r\n""")
	
	print("\n===*===*===*===*===*===*===*===*===*===*===*===*===*===*===*===*===*===*===*===")
	print("===*===*===*===*===*===*===*===*===*===*===*===*===*===*===*===*===*===*===*===\n")
print("\nfin")


# + ACK + retour d'info + gestion erreurs.

#def transmitter(info,): # priorite ? # destination ? 
	#active emission
	# stocke et formate les donnees
	#liste_envoie.append(donnees)
	# Si (peut transmettre)
		 # liste_envoie.push(donnees)
		 # transmet + ecoute
		 # si transmit + ACK
			# valide
		 # sinon , liste_envoie.append(donnees)
		
	
