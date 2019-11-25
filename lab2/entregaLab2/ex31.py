from Crypto.Cipher import AES
import binascii
import os, random, struct



filename = '2019_09_25_17_01_49_antonio.guilera.enc'
filekey = '2019_09_25_17_01_49_antonio.guilera.key'
output = 'decryptedPractica2Toni'

filename2 = '2019_09_25_17_02_05_lluis.marques.enc'
filekey2 = '2019_09_25_17_02_05_lluis.marques.key'
output2 = 'decryptedPractica2Lluis'

#bytesLast16 = b'\x1f\x03\xcav\xd0\x81\x92\xec`>\x13\xdf\x0c\x14\xb6r\xc0\xf9`\xb7\xdd'

#IV toni: b'\xad\xef\xae\xf2\xe1c\x07\xea@\x06\xf5\x0f\xa5\x0b\xcd\xe7'
#IV lluis: b"\x9c\xf7j\xa5\xb3\x10\xb0\xa0&g\xbd\xf9\x96'\x94<"

with open(filename, 'rb') as f:
	content = f.read()
	IV = content[:16]
		
with open(filekey, 'rb') as f:
	key = f.read()

def decrypt():		
	obj = AES.new(key, AES.MODE_CFB, IV)
	
	with open(output, 'wb') as f:
		f.write(obj.decrypt(content[16:]))
	

decrypt()

with open(filename2, 'rb') as f:
	content2 = f.read()
	IV2 = content2[:16]
		
with open(filekey2, 'rb') as f:
	key2 = f.read()

def decrypt2():		
	obj2 = AES.new(key2, AES.MODE_CFB, IV2)
	
	with open(output2, 'wb') as f:
		f.write(obj2.decrypt(content2[16:]))

decrypt2()

#decrypt_file(key, filename, output, 16) 
