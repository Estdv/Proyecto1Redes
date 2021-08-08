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


class Register(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.user = jid
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.disconnect()

    def register(self, iq):
        iq = self.Iq()
        iq['type'] = 'set'
        iq['register']['username'] = self.boundjid.user
        iq['register']['password'] = self.password

        try:
            iq.send()
            print("Nueva Cuenta Creada", self.boundjid,"\n")
        except IqError as e:
            print("Error en Registro ", e,"\n")
            self.disconnect()
        except IqTimeout:
            print("Timeout en el servidor")
            self.disconnect()
        except Exception as e:
            print(e)
            self.disconnect()  

    def delete_account(self):
        delete = self.Iq()
        delete['type'] = 'set'
        delete['from'] = self.user
        fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        delete.append(fragment)

        try:
            delete.send()
            print("Cuenta Borrada")
        except IqError as e:
            print("Error al borrar la cuenta", e)
        except IqTimeout:
            print("Timeout en el servidor")
        except Exception as e:
            print(e)






print("BIENVENIDO AL CHAT")
print("PRESIONE 1 PARA INGRESAR EN EL SERVIDOR DE ALUMCHAT")
print("PRESIONE 2 PARA REGISTRARSE EN EL SERVIDOR DE ALUMCHAT")
print("PRESIONE 3 PARA SALIR")

op = input("")

usu = ""
psd = ""

while (op != "3"):
     if(op== "1"):
          usu = input("Ingrese nuevo usuario: ")
          psd = getpass("Ingrese contraseña: ")

     elif(op == "2"):
          usu = input("Ingrese nuevo usuario: ")
          psd = getpass("Ingrese contraseña: ")
          xmpp = Register(usu, psd)
          xmpp.register_plugin('xep_0030') ### Service Discovery
          xmpp.register_plugin('xep_0004') ### Data Forms
          xmpp.register_plugin('xep_0066') ### Band Data
          xmpp.register_plugin('xep_0077') ### Band Registration
          xmpp.connect()
          xmpp.process(forever=False)
          print("Registro Completado\n")
     else:
          print("Opcion invalida intente denuevo")

     op2  = input("")
     while(op2 != "9"):
          if(op2 =="1"):
               print("mostrar contactos")

          elif(op2 == "2"):
               print("Agregar contacto")

          elif(op2 == "3"):
               print("MOstrar detalles de un contacto")

          elif(op2 == "4"):
               print("Chat 1 a 1")

          elif(op2 == "5"):
               print("Chat grupal")

          elif(op2 == "6"):
               print("Def mensaje de presencia")

          elif(op2 == "7"):
               xmpp = Register(usu, psd)
               xmpp.delete_account()
               xmpp = None
               control = False
               op2 = "9"

          elif(op2 == "8"):
               op2 = "9"
               op = "3"

          else:
               print("Opcion invalida intente denuevo")

print("GRACIAS HASTA LUEGO")
        
