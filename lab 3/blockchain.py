import random
import Crypto.Util.number
import sympy
import hashlib
from Crypto import Random

###############
#BLOC VALID --> hash h satisfà que h < 2**(256-d), d = proof of work, en aquesta practica, d = 16
# CALCUL DEL HASH:
# entrada = str(previous_block_hash)
# entrada = entrada + str(trasnaction.public_key.publicExponent)
# entrada = entrada + str(transaction.message)
# entrada = entrada + str(transaction.signature)
# entrada = entrada + str(seed)
# h = int(hashlib.sha256(entrada.enconde()).hexdigest(), 16)
###############

d = 16 #proof_of_work

class block:
	def __init__(self):
		'''
		crea un bloc (no té perqué ser vàlid)
		'''
		self.block_hash = 0 #block SHA256 actual
		self.previous_block_hash = 0 #block SHA256 del bloc anterior
		self.transaction = 0 #transacció valida
		self.seed = 0 #nombre enter
		
	def genesis(self, trans):
		'''
		PRE: transaction sempre es una transacció valida
		Genera el primer bloc duna cadena amb transaccio "transaction" que es caracteritza per:
		-previos_bloc_hash = 0
		-es valid
		'''
		self.transaction = trans
		self.previous_block_hash = 0
		#generate seed and hash in loop until it is valid!
		self.seed = random.randrange(0,2**256)
		self.block_hash = self.generate_hash()
		while(not self.verify_block()):
			self.seed = random.randrange(0, 2**256)
			self.block_hash = self.generate_hash()
		return self
		
		
	def generate_hash(self):
		aux = str(self.previous_block_hash)
		aux = aux + str(self.transaction.public_key.publicExponent)
		aux = aux + str(self.transaction.public_key.modulus)
		aux = aux + str(self.transaction.message)
		aux = aux + str(self.transaction.signature)
		aux = aux + str(self.seed)
		h = int(hashlib.sha256(aux.encode()).hexdigest(), 16)
		return h
	
	def next_block(self, trans):
		'''
		Genera el seguent block valid amb la transaccio "transaction"
		'''
		nblock = block()
		nblock.previous_block_hash = self.block_hash
		nblock.transaction = trans
		#generate seed and hash in loop until it is valid!
		nblock.seed = random.randrange(0,2**256)
		nblock.block_hash = nblock.generate_hash()
		while(not nblock.verify_block()):
			nblock.seed = random.randrange(0, 2**256)
			nblock.block_hash = nblock.generate_hash()
		return nblock
		
	def verify_block(self):
		'''
		Verifica si un bloc es valid:
		-Comprova que el hash del block anterior cumpleix les condicions exigides
		-comprova la transaccio del bloc es valida
		-comprova que el hash del bloc cumpleix las condicions exigides
		'''
		d = 16
		limit = 2**(256-d)
		#Check previous block hash
		h = self.previous_block_hash
		if(h >= limit): return False
		#Check transaction
		if(self.transaction.verify() == False): return False
		#Check current block hash
		h = self.block_hash
		if(h >= limit): 
			return False
		return True
		
### rsa gen -> https://asecuritysite.com/encryption/getprimen
		
class transaction:
	def __init__(self, message, RSAKey):
		'''
		Genera una transaccion signant "message" amb la clau "RSAKey"
		'''
		#genero public key con RSAKey
		#luego firmar con sign de rsakey
		self.public_key = rsa_public_key(RSAKey) #clau publica RSA corresponent a RSAKey (clau RSA amb la que es firma la transaccio)
		self.message = message #documet que es signa a la transaccio, representat per un enter
		self.signature = RSAKey.sign(message) #signatura del missatge feta amb el RSAKey representada per un enter
		
	def verify(self):
		'''
		Retorna TRUE si "signature" es correspon amb una signatura de "message" feta amb la clau publica "public_key". 
		Retona FALSE si no
		'''
		return self.public_key.verify(self.message, self.signature)
		
class rsa_key:
	def __init__(self, bits_module=2048, e=2**16+1):
		'''
		genera clau RSA de 2048 bits i exponent 2**16+1 per defecte
		'''
		self.bits_module = bits_module
		self.publicExponent = e #enter
		self.generate_primePQ()
		phi_n = (self.primeP - 1) * (self.primeQ - 1)
		self.modulus = self.primeP * self.primeQ #enter -> n = p*q
		#sympy gcdex(a,b) a la pos 0 retorna a**-1 mod (b)
		self.privateExponent = sympy.gcdex(self.publicExponent, phi_n)[0] #enter equivalent a d (referencia a les diapos)
		self.privateExponentModulusPhiP = self.privateExponent % (self.primeP - 1) #congruent amb privateExponent modul prime P - 1, enter
		self.privateExponentModulusPhiQ = self.privateExponent % (self.primeQ - 1)  #congruent amb privatExponent modul Prime Q - 1, enter
		self.inverseQModulusP = sympy.gcdex(self.primeQ, self.primeP)[0] #invers de primeQ^-1 modul primeP, enter
	
	def generate_primePQ(self):
		valid = 0;
		while(valid != 1):
			self.primeP = Crypto.Util.number.getPrime(self.bits_module//2, randfunc=Crypto.Random.get_random_bytes) #enter prim de 1024 bits
			self.primeQ = Crypto.Util.number.getPrime(self.bits_module//2, randfunc=Crypto.Random.get_random_bytes) #enter prim de 1024 bits
			valid = self.validate_PQ()
	
	def validate_PQ(self):
		phi_n = (self.primeP - 1) * (self.primeQ - 1)
		return gcd(self.publicExponent, phi_n) and self.primeP != self.primeQ
	
	def sign(self,message):
		'''
		https://www.geeksforgeeks.org/weak-rsa-decryption-chinese-remainder-theorem/
		retorna un enter que es la signatura del "message", feta amb la clau rsa fent servir el TXR
		'''
		m1 = pow(message, int(self.privateExponentModulusPhiP), self.primeP)
		m2 = pow(message, int(self.privateExponentModulusPhiQ), self.primeQ)
		h = (self.inverseQModulusP * (m1 - m2)) % self.primeP
		mFinal = m2 + h * self.primeQ
		return mFinal
	
	def sign_slow(self,message):
		'''
		m^d % n
		retorna un enter que es la signatura del "message", feta amb la clau RSA sense fer servir el TXR
		'''
		mFinal = pow(message, self.privateExponent, self.modulus) #(message**self.privateExponent) % self.modulus
		return mFinal
		
			
			###P o Q compartida con otros estudiantes (al menos 1 estudiante)
class rsa_public_key:
	def __init__(self, rsa_key):
		'''
		genera la clau publica RSA asociada a la clau RSA "rsa_key"
		'''
		self.publicExponent = rsa_key.publicExponent #exponent public de la clau RSA_KEY
		self.modulus = rsa_key.modulus #modul de la clau rsa_key
		
	def verify(self, message, signature):
		'''
		retorna TRUE si "signature" es correspon amb una signatura de "message" feta amb la clau RSA asociada a la clau publica RSA
		retorna FALSE si no
		'''
		return message == pow(signature, self.publicExponent, self.modulus)		

class block_chain:
	def __init__(self, trans):
		'''
		genera una cadena de blocs que es una llista de blocs, el primer bloc es un bloc "genesis" generat amb la transaccio "transaction"
		'''
		self.list_of_blocks = [block().genesis(trans)]
	
	def add_block(self, trans):
		'''
		afegeix a la llista de blocs un nou bloc valid generat amb la transaccio "transaction"
		'''
		act = self.list_of_blocks[-1]
		self.list_of_blocks.append(act.next_block(trans))
		
	def verify(self):
		'''
		Veritfica si la cadena de blocs es valida:
		-comprova que tots els blocs son valids
		-comprova que el pimer bloc es bloc "genesis"
		-comprova que per cada bloc de la cadena el seguent es el correcte
		Si totes les comprovacions son correctes retorna TRUE
		Retorna FALSE si no
		'''
		for b in self.list_of_blocks: 
			if b.verify_block() == False : return False
		return True
		
		
def gcd(a,b):
	if b > a:
		if b % a == 0:
			return a
		else:
			return gcd(b % a, a)
	else:
		if a % b == 0:
			return b
		else:
			return gcd(b, a % b)
		
def main():
	aver = rsa_key()
	#print(aver.primeP)
	#print(aver.primeQ)
	trans = transaction(1234, aver)
	listblocks = block_chain(trans)
	print('transaction signature: ')
	print(trans.signature)
	print('previous block hash: ')
	print(listblocks.list_of_blocks[-1].previous_block_hash)
	print('block seed: ')
	print(listblocks.list_of_blocks[-1].seed)
	print('block hash: ')
	print(listblocks.list_of_blocks[-1].block_hash)
	print('Verified trans? : ')
	print(listblocks.list_of_blocks[-1].verify_block())
	print('-------------------------------------------------------------------------------------------------')
	for i in range(0,5):
		aver = rsa_key()
		#print(aver.primeP)
		#print(aver.primeQ)
		trans = transaction(i*4321+1, aver)
		#print(trans.verify())
		#bloc = block().genesis(trans)
		listblocks.add_block(trans)
		print('transaction signature: ')
		print(trans.signature)
		print('previous block hash: ')
		print(listblocks.list_of_blocks[-1].previous_block_hash)
		print('block seed: ')
		print(listblocks.list_of_blocks[-1].seed)
		print('block hash: ')
		print(listblocks.list_of_blocks[-1].block_hash)
		print('Verified trans? : ')
		print(listblocks.list_of_blocks[-1].verify_block())
		print('----------------------------------------------------------------------------------------------------')
	print("list verified: ")
	print(listblocks.verify())
	
main()	
