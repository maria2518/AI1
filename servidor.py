import socket
import threading
import sys
import pickle
import os

class Servidor():
# Para que el usuario pueda introducir el puerto usamos el input
# Guardamos el puerto dentro de la variable "puerto"
	def __init__(self, host=socket.gethostname(), puerto=int(input("Introduzca el puerto que desea utilizar: "))):
		self.clientes = []
# Para poder saber la direccion IP a la que se conecta el servidor usaremos "socket.gethostbyname(host)" 
		print("\n Su IP es: ",socket.gethostbyname(host))
		print("\n Su puerto es: ", puerto, "\n")
		self.sock = socket.socket()
		self.sock.bind((str(host), int(puerto)))
		self.sock.listen(20)
		self.sock.setblocking(False)

		aceptar = threading.Thread(target=self.aceptarC)
		procesar = threading.Thread(target=self.procesarC)
		
		aceptar.daemon = True
		aceptar.start()

		procesar.daemon = True
		procesar.start()

		while True:
			msg = input('SALIR = Q\n')
			if msg == 'Q':
				print("Hasta luego, vuelva pronto")
				self.sock.close()
				sys.exit()
			else:
				pass

	def broadcast(self, msg, cliente):
		for c in self.clientes:
			try:
				if c != cliente:
					c.send(msg)
			except:
				self.clientes.remove(c)

	def aceptarC(self):
		while True:
			try:
				conn, addr = self.sock.accept()
				print(f"\nConexion aceptada via {conn}\n")
				conn.setblocking(False)
				self.clientes.append(conn)
			except:
				pass
# Para poder escribir los datos en el fichero creamos la siguiente función             
	def escribir(self, msg):
		f=open("u22072362AI1.txt", "a")
		f.write(msg + "\n")
		f.close()

	def procesarC(self):
		print("Procesamiento de mensajes iniciado")
		while True:
			if len(self.clientes) > 0:
				for c in self.clientes:
					try:
						data = c.recv(32)
						if data:
							self.broadcast(data,c)
# Se llama a la función escribir y se le pasan los datos.
							self.escribir(pickle.loads(data))
					except:
						pass

s = Servidor()