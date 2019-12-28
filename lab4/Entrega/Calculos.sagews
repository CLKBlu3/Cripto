︠9a3ce036-739a-481a-bb35-a7f311697c3ds︠

#Params de la curva 256
p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
n = 115792089210356248762697446949407573529996955224135760342422259061068512044369

#la a es -3
#la b es propia de la curva

a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b


E = EllipticCurve(Zmod(p),[a,b])
#E.cardinality()
#E.cardinality().is_prime()

#Punto a partir de la clave publica
x = 0x23551f0b79e4822143c07d2b3f4570a67ed537197fe77ff14acdb3d220021724
y = 0x19b80ac6d1582b114cfafa89bab7ab1b8acaaeacbad7e3588fc94aa406279e9c
G = E([x,y])
#G.order()

#Verificacion de la signatura

F1 = 0x00880cddcd74b943a7ee9f1d774fb207160391881b7ffafe9c477f76094c29cd63
F2 = 0x363a9ef9afed040a05a373123a70f87456e4698c7bfebc9f834d60b2b34f4243

#m son los 256 primeros bits del sha384 de la concatenacion de los 6 binarios que hemos obtenido con wireshark
m = 0xB2A44C8DB04CEF601AEFE60F28BF4E7BD512D80E7E1EE060AA4BDCA617D321FF
mentera = 0xB2A44C8DB04CEF601AEFE60F28BF4E7BD512D80E7E1EE060AA4BDCA617D321FF7D76E01F7C5F6591D17854C9C0216938



#Punto q nos da el NIST

x1 = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
y1 = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
Punto = E([x1,y1])
#Punto.order()



w1 = mod(m*F2^-1,n)
w2 = mod(F1*F2^-1,n)

verificacion = Integer(w1)*Punto+G*Integer(w2)
mod(verificacion[0],n) == F1


︡ef1577eb-2101-44c1-b357-f141efe5b5f6︡{"stdout":"True\n"}︡{"done":true}
︠b84dcbe4-1aee-4d07-acc4-9203999ec935︠

︡46dd6d9f-d828-4b35-a9ca-ab515dbb8ef0︡{"done":true}









