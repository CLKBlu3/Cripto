import binascii
filename = '2019_09_25_17_02_05_lluis.marques.key'
with open(filename, 'rb') as f:
    content = f.read()#[-16:]
print(content.hex())
print(len(content.hex()))

