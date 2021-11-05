import threading
import sys
import socket
import pickle
import os

class Cliente():
# Para que el usuario pueda introducir el puerto y la IP dada por el servidor usamos el input
	def __init__(self, host=input("Introduzca la IP dada por el servidor: "), puerto=int(input("Introduzca el puerto del servidor: ")), nombre=input("Introduzca su nombre: ")):
		self.nombre = nombre
		self.sock = socket.socket()
		self.sock.connect((str(host), int(puerto)))
		hilo_recv_mensaje = threading.Thread(target=self.recibir)
		hilo_recv_mensaje.daemon = True
		hilo_recv_mensaje.start()
		print('Hilo con PID',os.getpid())
		print('Hilos activos', threading.active_count())

		while True:
			msg = input('\nEscriba texto ? ** Enviar = ENTER ** Abandonar Chat = Q \n')
			if msg != 'Q' :
# Para poder enviar el mensage con el formato nombre:mensage hacemos lo siguiente:
				self.enviar(nombre + ": " + msg)
			else:
				print("Hasta luego")
				self.sock.close()
				sys.exit()

	def recibir(self):
		while True:
			try:
				data = self.sock.recv(32)
				if data:
					print(pickle.loads(data))
			except:
				pass

	def enviar(self, msg):
		self.sock.send(pickle.dumps(msg))

c = Cliente()