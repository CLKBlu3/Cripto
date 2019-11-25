from Crypto.Cipher import AES
import secrets

def cuentaCeros(data):
	#.encode('utf-8')
	data = int.from_bytes(data, 'big')
	data = bin(data)[2:] #remove 0b del output como string de data
	return 128-len(data) #si hay 0 al principio los elimina asi que la diferencia con 128 son los 0s que hay.

def proc():
	maximCount = 0
	messageMax = 0
	keyMax = 0
	auxCeros = 0
	for i in range (3000000):
			messageAux = secrets.token_bytes(16)
			keyAux = secrets.token_bytes(16)
			aes = AES.new(keyAux)
			cif = aes.encrypt(messageAux)
			auxCeros = cuentaCeros(cif)
			if(auxCeros > maximCount):
				maximCount = auxCeros
				messageMax = messageAux
				keyMax = keyAux
	print("Numero de ceros : " + str(maximCount) + " Con el mensaje : " + str(messageMax.hex()) + " y la clave " + str(keyMax.hex()))

proc()    
               







