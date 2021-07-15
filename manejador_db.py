from tinydb import TinyDB, where
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np


class manejador_db: 
	
	def agregar_num(self, estampa, numero, sesion, valor, nivelNum):
		db=TinyDB("numeros.json")
		lista=db.search(where("estampa")==estampa)
		if(len(lista)==0):
			db.insert({"estampa":estampa, "numero":numero,"nivel": valor,"nNum": nivelNum,"sesion": sesion})
			
	def consultarTodo(self):
		db=TinyDB("numeros.json")
		lista=db.all()
		cad='<table border="2">'
		for elem in lista:
			cad=cad+"<tr><td>Estampa</td><td>"+str(elem["estampa"])+"</td></tr>"
			cad=cad+"<tr><td>Valor dB</td><td>"+str(elem["numero"])+"</td></tr>"
			cad=cad+"<tr><td>Nivel</td><td>"+str(elem["nivel"])+"</td></tr>"
			cad=cad+"<tr><td>Sesion</td><td>"+str(elem["sesion"])+"</td></tr>"
			cad=cad+"<tr><td bgcolor='black' colspan='2'></td></tr>"
		cad=cad+"</table>"
		return cad
	
	def initSesion(self):
		db=TinyDB("numeros.json")
		lista=db.all()
		num=0
		for elem in lista:
			if int(elem['sesion']) > num:
				num=int(elem['sesion'])

		return str(num)
			
	def consultarSesion(self, sesion):
		db=TinyDB("numeros.json")
		lista=db.search(where("sesion")==sesion)
		cad="<table border='2'>"
		for elem in lista:
			cad=cad+"<tr><td>Estampa</td><td>"+str(elem["estampa"])+"</td></tr>"
			cad=cad+"<tr><td>Valor dB</td><td>"+str(elem["numero"])+"</td></tr>"
			cad=cad+"<tr><td>Nivel</td><td>"+str(elem["nivel"])+"</td></tr>"
			cad=cad+"<tr><td>Sesion</td><td>"+str(elem["sesion"])+"</td></tr>"
			cad=cad+"<tr><td bgcolor='black' colspan='2'></td></tr>"			
		cad=cad+"</table>"
		return cad
		
	def centro1(self, sesion):
		db=TinyDB("numeros.json")
		lista=db.search(where("sesion")==sesion)
		aux=[]
		auxa=[]
		for elem in lista:
			aux.append([elem["numero"],elem["nNum"]])
			
		kmeans=KMeans(n_clusters=2)
		kmeans.fit(aux)
		centroides= kmeans.cluster_centers_
		lista =centroides.tolist()
		
		for elem in lista:
			auxa.append(elem[0])
			
		cad=str(auxa[0])+";"+str(auxa[1])
		cad=cad.strip()
		return cad
		
	def centro2(self, sesion):
		db=TinyDB("numeros.json")
		lista=db.search(where("sesion")==sesion)
		aux=[]
		auxa=[]
		for elem in lista:
			aux.append([elem["numero"],elem["nNum"]])
			
		kmeans=KMeans(n_clusters=2)
		kmeans.fit(aux)
		centroides= kmeans.cluster_centers_
		lista =centroides.tolist()
		
		for elem in lista:
			auxa.append(elem[1])
			
		cad=str(auxa[0])+";"+str(auxa[1])
		cad=cad.strip()
		return cad
		
	def val(self, sesion):
		db=TinyDB("numeros.json")
		lista=db.search(where("sesion")==sesion)
		aux=[]
		auxy=[]
		for elem in lista:
			aux.append(elem["nNum"])
			auxy.append(elem["numero"])
			
		cad=str(aux)+";"+str(auxy)
		cad=cad.replace("[","")
		cad=cad.replace("]","")
		cad=cad.strip()
		return cad
	
	def analisis(self, sesion):
		db=TinyDB("numeros.json")
		lista=db.search(where("sesion")==sesion)
		aux=[]
		auxnr=[]
		auxclas=[]
		cont=0
		nr=0
		clas=0
		n1=0
		n2=0
		n3=0
		n4=0
		n5=0
		n6=0
		for elem in lista:
			aux.append([elem["numero"],elem["nNum"]])
			auxnr.append([elem['numero']])
			auxclas.append([elem['nNum']])
			nr=nr+float(elem['numero'])
			clas=clas+elem["nNum"]
			cont=cont+1
			if elem['nNum']==1:
				n1=n1+1
			if elem['nNum']==2:
				n2=n2+1
			if elem['nNum']==3:
				n3=n3+1
			if elem['nNum']==4:
				n4=n4+1
			if elem['nNum']==5:
				n5=n5+1
			if elem['nNum']==6:
				n6=n6+1
			
						
		kmeans=KMeans(n_clusters=2)
		kmeans.fit(aux)
		centroides= kmeans.cluster_centers_		
		
		
		cad ="<center><table border='2'>"
		cad=cad+"<tr><td bgcolor=#F5B7B1 colspan='2'><center>Centroides</center></td></tr>"	
		cad= cad+"<tr><td><center>Nivel de ruido </center></td><td><center>Clasificación</center></td></tr>"
		
		for elem in centroides:
			cad=cad+"<tr><td>"+str(elem[0])+"</td><td>"+str(elem[1])+"</td></tr>"
		n=np.array(auxnr)
		n = np.array(n, dtype=np.float64)
		cad= cad+"<tr><td bgcolor=#F5B7B1 colspan='2'><center>Desviación Estandar</center></td></tr>"
		cad= cad+"<tr><td><center>Nivel de ruido </center></td><td><center>Clasificación</center></td></tr>"
		cad= cad+"<tr><td><center>"+str(np.std(n))+"</center></td><td><center>"+str(np.std(auxclas))+"</center></td></tr>"

		cad= cad+"<tr><td bgcolor=#F5B7B1 colspan='2'><center>Promedio</center></td></tr>"
		cad= cad+"<tr><td><center>Nivel de ruido </center></td><td><center>Clasificación</center></td></tr>"
		cad= cad+"<tr><td><center>"+str(nr/cont)+"</center></td><td><center>"+str(clas/cont)+"</center></td></tr>"
		
		cad= cad+"<tr><td bgcolor=#F5B7B1 colspan='2'><center>Clasificación</center></td></tr>"
		cad= cad+"<tr><td><center>Bajo</center></td><td><center>"+ str(n1)+"</center></td></tr>"
		cad= cad+"<tr><td><center>Normal</center></td><td><center>"+ str(n2)+"</center></td></tr>"
		cad= cad+"<tr><td><center>Cosiderable</center></td><td><center>"+ str(n3)+"</center></td></tr>"
		cad= cad+"<tr><td><center>Alto</center></td><td><center>"+ str(n4)+"</center></td></tr>"
		cad= cad+"<tr><td><center>Muy Alto</center></td><td><center>"+ str(n5)+"</center></td></tr>"
		cad= cad+"<tr><td><center>Umbral de dolor</center></td><td><center>"+ str(n6)+"</center></td></tr>"
		cad= cad+"<tr><td><center>Total de datos</center></td><td><center>"+ str(cont)+"</center></td></tr>"
			
		cad= cad+"</tabla></center>"
		return cad
