from flask import Flask, request, render_template
from manejador_db import manejador_db
import math
import random
import time
import requests

app = Flask(__name__)
man=manejador_db()

@app.route("/")
def home():
	tit="Monitoreo de Sonido"
	return render_template("index2.html",tit=tit)
	
	
@app.route("/aleatorio")
def aleatorio():
	cons=0
	constr=""
	response = requests.get('Http://192.168.0.9/') 
	#response = requests.get('http://192.168.1.112/') 
	estampa=time.time()
	resp=response.text
	response.close()
	ses=str(request.args["userSesion"])
	if float(resp) <=30:
		cons=1 #bajo
		constr="Bajo"
	if (float(resp)>30) and (float(resp)<=50):
		cons=2 #normal
		constr="Normal"
	if (float(resp)>50) and (float(resp)<=75):
		cons=3 #Considerable
		constr="Cosiderable"
	if (float(resp)>75) and (float(resp)<=100):
		cons=4 #Alto
		constr="Alto"
	if (float(resp)>100) and (float(resp)<=120.5):
		cons=5 #Muy alto
		constr="Muy alto"
	if (float(resp)>120.5):
		cons=6 #Umbral de dolor
		constr="Umbral de dolor"
	print(response.text)
	print(estampa)
	print(ses)
	man.agregar_num(estampa, resp, ses, constr, cons)
	return "{\"num\":"+resp+",\"cadena\":"+str(cons)+"}"

@app.route("/consultar")
def consultar():
	return man.consultarTodo()

@app.route("/buscar")
def buscar():
	sesion=request.args['busqueda']
	return man.consultarSesion(sesion)
	
@app.route("/sesion")
def sesion():
	return man.initSesion()
	
@app.route("/centroide")
def centroide():
	sesion=request.args['busqueda']
	return man.analisis(sesion)
	
@app.route("/valorxy")
def valxy():
	sesion=request.args['busqueda']
	return man.val(sesion)
	
@app.route("/c1")
def c1():
	sesion=request.args['busqueda']
	return man.centro1(sesion)
	
@app.route("/c2")
def c2():
	sesion=request.args['busqueda']
	return man.centro2(sesion)

if __name__ == "__main__":
	app.run("0.0.0.0")



