tabla_exp = []
tabla_log = [0 for _ in range(256)]

def xor_sum(a,b):
	return a ^ b

def xor_mul(a,b): 
	#https://crypto.stackexchange.com/questions/63139/how-to-do-hexadecimal-multiplication-in-gf28 
	#https://en.wikipedia.org/wiki/Finite_field_arithmetic
	c = 0
	for _ in bin(b)[:1:-1]:
		c^=int(_)*a
		a<<=1
		if(a>255): a=a^0x11B
	return c

def GF_product_p(a,b):
	#pre: a i b enters en el rang [0,255]
	#polinomi usat per les ops: m = x^8 + x^4 + x^3 + x^2 + 1 (100011101) = 285
	r = xor_mul(a, b)
	return r #hex(r)

#part1
print("Xor mul: ")
print(xor_mul(0x02,0x7F))
#print("Xor sum: ")
#print(xor_sum(244,213))
#print("Xor product with modulus: ")
#print(GF_product_p(0x57,0x83))

#part2
def mcd(a, b):
	exc = 0
	while(b > 0):
		exc = b
		b = a % b
		a = exc
	return a

def GF_es_generador(a):
	#pre: a element del cos representat per enters [0,255]
	#post: true si es generador, false otherwise
	return (mcd(tabla_log[a],255) == 1)

#https://www.pclviewer.com/rs2/galois.html
#https://iagolast.github.io/blog/2016/11/07/implementacion-gf55.html

def GF_tabla_exp():
	#print(len(tabla_log))
	last = 1
	tabla_exp.append(1)
	for i in range(1,255):
		last = GF_product_p(last, 2)
		tabla_exp.append(last)
		tabla_log[last] = i
	return tabla_exp
	
def GF_tabla_log():
	return tabla_log
	
def GF_product_t(a, b):
	#pre: a i b en el cos [0,255]
	if(a == 0 or b == 0): return 0
	if(a == 1): return b
	if(b == 1): return a
	return tabla_exp[(tabla_log[a] + tabla_log[b])%255]

def GF_invers(a):
	#pre: a del cos [0,255]
	if(a == 0): return -1 #error!
	return tabla_exp[255-tabla_log[a]]
 
#print("Part2, comprovar generador: a = 3")
print(GF_tabla_exp()) #generem la taula exponencial
print(GF_tabla_log())
print(GF_es_generador(8))
#print("Mult de taules:")
#print(GF_product_t(3,3))
print("Inversa:")
print(GF_invers(3))

import time

def measureTime(a):
	text_file = open('comparativa.txt','w+')
	text_file.write("a value: ")
	text_file.write(str(a) + '\n')

	start = time.clock()
	GF_product_p(a, 0x02)
	elapsed = time.clock()
	elapsed = elapsed - start
	text_file.write("Time spent in function gp_product_p(a, 0x02) = ")
	text_file.write(str(elapsed) + '\n')
	start = time.clock()
	GF_product_t(a, 0x02)
	elapsed = time.clock()
	elapsed = elapsed - start
	text_file.write("Time spent in function gp_product_t(a, 0x02) = ")
	text_file.write(str(elapsed) + '\n')


	start = time.clock()
	GF_product_p(a, 0x03)
	elapsed = time.clock()
	elapsed = elapsed - start
	text_file.write("Time spent in function gp_product_p(a, 0x03) = ")
	text_file.write(str(elapsed) + '\n')
	start = time.clock()
	GF_product_t(a, 0x03)
	elapsed = time.clock()
	elapsed = elapsed - start
	text_file.write("Time spent in function gp_product_t(a, 0x03) = ")
	text_file.write(str(elapsed) + '\n')

	start = time.clock()
	GF_product_p(a, 0x09)
	elapsed = time.clock()
	elapsed = elapsed - start
	text_file.write("Time spent in function gp_product_p(a, 0x09) = ")
	text_file.write(str(elapsed) + '\n')
	start = time.clock()
	GF_product_t(a, 0x09)
	elapsed = time.clock()
	elapsed = elapsed - start
	text_file.write("Time spent in function gp_product_t(a, 0x09) = ")
	text_file.write(str(elapsed) + '\n')

	start = time.clock()
	GF_product_p(a, 0x0B)
	elapsed = time.clock()
	elapsed = elapsed - start
	text_file.write("Time spent in function gp_product_p(a, 0x0B) = ")
	text_file.write(str(elapsed) + '\n')
	start = time.clock()
	GF_product_t(a, 0x0B)
	elapsed = time.clock()
	elapsed = elapsed - start
	text_file.write("Time spent in function gp_product_t(a, 0x0B) = ")
	text_file.write(str(elapsed) + '\n')

	start = time.clock()
	GF_product_p(a, 0x0D)
	elapsed = time.clock()
	elapsed = elapsed - start
	text_file.write("Time spent in function gp_product_p(a, 0x0D) = ")
	text_file.write(str(elapsed) + '\n')
	start = time.clock()
	GF_product_t(a, 0x0D)
	elapsed = time.clock()
	elapsed = elapsed - start
	text_file.write("Time spent in function gp_product_t(a, 0x0D) = ")
	text_file.write(str(elapsed) + '\n')

	start = time.clock()
	GF_product_p(a, 0x0E)
	elapsed = time.clock()
	elapsed = elapsed - start
	text_file.write("Time spent in function gp_product_p(a, 0x0E) = ")
	text_file.write(str(elapsed) + '\n')
	start = time.clock()
	GF_product_t(a, 0x09)
	elapsed = time.clock()
	elapsed = elapsed - start
	text_file.write("Time spent in function gp_product_t(a, 0x0E) = ")
	text_file.write(str(elapsed) + '\n')
	
	text_file.close()
	return

#print(measureTime(0x24))





