from Crypto.Cipher import AES
from hashlib import sha256
import os

filename = '2019_09_25_17_01_49_antonio.guilera.puerta_trasera.enc'
output = 'decryptedPractica23Toni'

filename2 = '2019_09_25_17_02_05_lluis.marques.puerta_trasera.enc'
output2 = 'decryptedPractica23Lluis'

ivToni = "a2c55e13f3a28b2d7754928891f5fb22"

def decrypt(key, content, iv, outfile = output):		
	obj = AES.new(key, AES.MODE_CBC, iv)
	content = obj.decrypt(content)
	if(int(content[-1]) >= 1 and int(content[-1]) <= 16):
		content = content[:-ord(chr(content[-1]))]
		#print("hola")
		with open(outfile, 'wb') as f:
			f.write(content)
			f.close()
			return 0
	else: return -1

def check(clave, content, iube, outfile = output):
	Hash = sha256(clave.encode('utf-8')).digest()
	HashKey = Hash[:16]
	HashIv = Hash[-16:]
	if(decrypt(HashKey,content, HashIv, outfile) == 0):
		#check magic numba and return true if valid?
		cmd = 'file ' + outfile
		res = os.popen(cmd).read()
		if(res.find('data') == -1): 
			print(res)
			print('key ' + str(clave.encode('utf-8')) + ' hashKey ' + str(HashKey) + ' HashIV ' + str(HashIv))
			return 1
	return 0

def backdoor():
	with open(filename, 'rb') as f:
		content = f.read()
		IV = content[:16]
	with open(filename2, 'rb') as f:
		content2 = f.read()
		IV2 = content2[:16]
		
	for i in range(128):
		#print(i)
		for j in range(128):
			clave = chr(i)*8 + chr(j)*8
			if(check(clave, content, IV, output) == 1): print('----------------------------------------------')
			#if(check(clave,content2, IV2, output2) == 1): print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

#backdoor()


#with open(filename2, 'rb') as f:
#		content2 = f.read()
#		IV2 = content2[:16]

#decrypt(b"\xb4L\x0b\xa9cva\\'\xfe\xf2F\x91\x82\xa6\x88", content2, b"\xfe\x98R\xd2'a;\xc7\x81\xa3j\x7f?\xd0j\x1d", output2)
			
with open(filename, 'rb') as f:
		content = f.read()
		IV = content[:16]

decrypt(b'\xdb\xd1\xa9\xab\xe6O\xd5Y\xf49\xa7K\xa3\xc6\xe8\xf8', content, b'`\x8a\xff\\\x7fmx\x0b\x0b4\xe5\x87a\x8c\x98\x95', output)
