#UVG
#Redes
#Proyecto 1

#Esteban Del Valle 18221

#Implementacion de xmpp en un cliente

import sys
import aiodns
import asyncio
import logging
from getpass import getpass
from argparse import ArgumentParser
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
import slixmpp
import base64, time
import threading


if sys.platform == 'win32' and sys.version_info >= (3, 8):
     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


print("BIENVENIDO AL CHAT")
print("PRESIONE 1 PARA REGISTRARSE EN EL SERVIDOR DE ALUMCHAT")
print("PRESIONE 2 PARA REGISTRARSE EN EL SERVIDOR DE ALUMCHAT")
print("PRESIONE 3 PARA SALIR")

op = input("")

while (op != "3"):
    if(op== "1"):
        #login

    elif(op == "2"):
        #Register

    else:
        print("Opcion invalida intente denuevo")

    while(op2 != "9"):

        if(op2 =="1"):
            #mostrar contactos

        elif(op2 == "2"):
            #Agregar contacto

        elif(op2 == "3"):
            #MOstrar detalles de un contacto

        elif(op2 == "4"):
            #Chat 1 a 1

        elif(op2 == "5"):
            #Chat grupal

        elif(op2 == "6"):
            #Def mensaje de presencia

        elif(op2 == "7"):
            #Eliminar cuenta

        elif(op2 == "8"):
            op2 = "9"
            op = "3"

        else:
            print("Opcion invalida intente denuevo")

print("GRACIAS HASTA LUEGO")
        
