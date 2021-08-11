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


#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+
#Clase Para Registro y Eliminacion de Cuenta          
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+
     
class RyE(slixmpp.ClientXMPP):
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


#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+
#Clase Para Registro y Eliminacion de Cuenta          
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+

class Del(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.user = jid
        self.add_event_handler("session_start", self.start)

    def start(self, event):
  
        self.send_presence()
        self.get_roster()

        delete = self.Iq()
        delete['type'] = 'set'
        delete['from'] = self.user
        fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        delete.append(fragment)

        try:
            delete.send()
            print("Cuenta Borrada")
        except IqError as e:
           
            print("Error", e)
        except IqTimeout:

            print("timeout del server")
        except Exception as e:
     
            print(e)  

        self.disconnect()



#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+
# Clase Para Contactos e Informacion        
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+

class Roster(slixmpp.ClientXMPP):
    def __init__(self, jid, password, user=None, show=True, message=""):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.presences = threading.Event()
        self.contacts = []
        self.user = user
        self.show = show
        self.message = message

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

        my_contacts = []
        try:
            self.get_roster()
        except IqError as e:
            print("Error", e)
        except IqTimeout:
            print("Timeout en el Server")
        
        self.presences.wait(3)

        my_roster = self.client_roster.groups()
        for group in my_roster:
            for user in my_roster[group]:
                status = show = answer = priority = ''
                self.contacts.append(user)
                subs = self.client_roster[user]['subscription']
                conexions = self.client_roster.presence(user)
                username = self.client_roster[user]['name'] 
                for answer, pres in conexions.items():
                    if pres['show']:
                        show = pres['show']
                    if pres['status']:
                        status = pres['status']
                    if pres['priority']:
                        status = pres['priority']

                my_contacts.append([
                    user,
                    subs,
                    status,
                    username,
                    priority
                ])
                self.contacts = my_contacts

        if(self.show):
            if(not self.user):
                if len(my_contacts)==0:
                    print('No hay usuarios conectados')
                else:
                    print('Usuarios: \n')
                for contact in my_contacts:
                    print('\tusuario:' , contact[0] , '\t\tStatus:' , contact[2])
            else:
                print('\n\n')
                for contact in my_contacts:
                    if(contact[0]==self .user):
                        print('\tUsuario:' , contact[0] , '\n\tStatus:' , contact[2] , '\n\tNombre:' , contact[3])
        else:
            for JID in self.contacts:
                self.notification_(JID, self.message, 'active')

        self.disconnect()

    def notification_(self, to, body, my_type):

        message = self.Message()
        message['to'] = to
        message['type'] = 'chat'
        message['body'] = body

        if (my_type == 'active'):
            fragmentStanza = ET.fromstring("<active xmlns='http://jabber.org/protocol/chatstates'/>")
        elif (my_type == 'composing'):
            fragmentStanza = ET.fromstring("<composing xmlns='http://jabber.org/protocol/chatstates'/>")
        elif (my_type == 'inactive'):
            fragmentStanza = ET.fromstring("<inactive xmlns='http://jabber.org/protocol/chatstates'/>")
        message.append(fragmentStanza)

        try:
            message.send()
        except IqError as e:
            print("Error", e)
        except IqTimeout:
            print("Timeout en el servidor")


#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+
# Clase Para Agregar Contactos      
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+

class Agregar(slixmpp.ClientXMPP):
    def __init__(self, jid, password, to):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.to = to

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        try:
            self.send_presence_subscription(pto=self.to) 
        except IqTimeout:
            print("Timeout del server") 
        self.disconnect()



#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+
# Clase Para Enviar mensajes   
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+

class MSG(slixmpp.ClientXMPP):
     def __init__(self, jid, password, recipient, message):
          slixmpp.ClientXMPP.__init__(self, jid, password)
          self.recipient = recipient
          self.msg = message
          self.add_event_handler("session_start", self.start)
          self.add_event_handler("message", self.message)

     async def start(self, event):
          self.send_presence()
          await self.get_roster()
          self.send_message(mto=self.recipient,mbody=self.msg,mtype='chat')


     def message(self, msg):
          
          if msg['type'] in ('chat'):
          
               recipient = msg['from']
               body = msg['body']
               print(str(recipient) +  ": " + str(body))
               message = input("Mensaje: ")
               self.send_message(mto=self.recipient,mbody=message)
                    


#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+
# Clase Para Chat grupal
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+

class Grupo(slixmpp.ClientXMPP):

    def __init__(self, jid, password, room, nick):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.jid = jid
        self.room = room
        self.nick = nick

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("muc::%s::got_online" % self.room,self.muc_online)

    async def start(self, event):

        await self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].join_muc(self.room, self.nick)

        message = input("Write the message: ")
        self.send_message(mto=self.room, mbody=message, mtype='groupchat')

    def muc_message(self, msg):
        if(str(msg['from']).split('/')[1]!=self.nick):
            print(str(msg['from']).split('/')[1] + ": " + msg['body'])
            message = input("Mensaje: ")
            self.send_message(mto=msg['from'].bare, mbody=message, mtype='groupchat')



#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+
# Clase Para Enviar archivos
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+

class Archivos(slixmpp.ClientXMPP):

    def __init__(self, jid, password, receiver, filename):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.receiver = receiver

        self.file = open(filename, 'rb')
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        try:
            #Set the receiver
            proxy = await self['xep_0065'].handshake(self.receiver)
            while True:
                data = self.file.read(1048576)
                if not data:
                    break
                await proxy.write(data)

            proxy.transport.write_eof()
        except (IqError, IqTimeout) as e:
            print('Timeout', e)
        else:
            print('Procedimiento terminado')
        finally:
            self.file.close()
            self.disconnect()


#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+
# Clase Para Notificaciones
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+
class Noti(slixmpp.ClientXMPP):

    def __init__(self, jid, password, user, message, type_):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.message = message
        self.user = user
        self.type_ = type_

    async def start(self, event):
        
        self.send_presence()
        await self.get_roster()

     
        self.notification_(self.user, self.message, 'active')

    def notification_(self, to, body, my_type):
        
        message = self.Message()
        message['to'] = to
        message['type'] = self.type_
        message['body'] = body

        if (my_type == 'active'):
            fragmentStanza = ET.fromstring("<active xmlns='http://jabber.org/protocol/chatstates'/>")
        elif (my_type == 'composing'):
            fragmentStanza = ET.fromstring("<composing xmlns='http://jabber.org/protocol/chatstates'/>")
        elif (my_type == 'inactive'):
            fragmentStanza = ET.fromstring("<inactive xmlns='http://jabber.org/protocol/chatstates'/>")
        message.append(fragmentStanza)

        try:
            message.send()
        except IqError as e:
            print("Error", e)
        except IqTimeout:
            print("Timeout")

    def message(self, msg):
        recipient = msg['from']
        body = msg['body']
        print(str(recipient) +  ": " + str(body))





#Final de definicion de clases
            
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

#Programa Principal

print("")
print("======================================================")
print("BIENVENIDO AL CHAT")
print("PRESIONE 1 PARA INGRESAR EN EL SERVIDOR DE ALUMCHAT")
print("PRESIONE 2 PARA REGISTRARSE EN EL SERVIDOR DE ALUMCHAT")
print("PRESIONE 3 PARA SALIR")
print("")
op = input("Opcion: ")
print("======================================================")
print("")
print("")
print("")

usu = ""
psd = ""

while (op != "3"):
     if(op== "1"):
          usu = input("Ingrese usuario: ")
          psd = getpass("Ingrese contraseña: ")

     elif(op == "2"):
          usu = input("Ingrese nuevo usuario: ")
          psd = getpass("Ingrese contraseña: ")
          xmpp = RyE(usu, psd)
          xmpp.register_plugin('xep_0030') ### Service Discovery
          xmpp.register_plugin('xep_0004') ### Data Forms
          xmpp.register_plugin('xep_0066') ### Band Data
          xmpp.register_plugin('xep_0077') ### Band Registration
          xmpp.connect()
          xmpp.process(forever=False)
          print("Registro Completado\n")
     else:
          print("Opcion invalida intente denuevo")

     print("")
     print("-----------------------------------------------")
     print("Presione 1 para mostrar contactos")
     print("Presione 2 para agregar contactos")
     print("Presione 3 para mostrar detalles de un contacto")
     print("Presione 4 para entrar a un chat 1 a 1")
     print("Presione 5 para entrar a un chat grupal")
     print("Presione 6 para cambiar mensaje de presencia")
     print("Presione 7 para enviar y recibir archivos")
     print("Presione 8 para notificaciones")
     print("Presione 9 para eliminar cuenta")
     print("Presione 10 para cerrar sesion")
     print("-----------------------------------------------")
     print("")

     op2  = input("")

     
     while(op2 != "10"):
          
          if(op2 =="1"):
               xmpp = Roster(usu, psd)
               xmpp.register_plugin('xep_0030') # Service Discovery
               xmpp.register_plugin('xep_0199') # XMPP Ping
               xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
               xmpp.register_plugin('xep_0096') # Jabber Search
               xmpp.connect()
               xmpp.process(forever=False)

          elif(op2 == "2"):
               con = input("Escriba el Usuario del contacto: ") 
               xmpp = Agregar(usu, psd, con)
               xmpp.register_plugin('xep_0030') # Service Discovery
               xmpp.register_plugin('xep_0199') # XMPP Ping
               xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
               xmpp.register_plugin('xep_0096') # Jabber Search
               xmpp.connect()
               xmpp.process(forever=False)


          elif(op2 == "3"):
               con = input("Escriba el Usuario del contacto: ") 
               xmpp = Roster(usu, psd, con)
               xmpp.register_plugin('xep_0030') # Service Discovery
               xmpp.register_plugin('xep_0199') # XMPP Ping
               xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
               xmpp.register_plugin('xep_0096') # Jabber Search
               xmpp.connect()
               xmpp.process(forever=False)


          elif(op2 == "4"):
               try:
                    cont = input("Ingrese el recipiente: ") 
                    msg = input("Mensaje: ")
                    xmpp = MSG(usu, psd, cont, msg)
                    xmpp.register_plugin('xep_0030') # Service Discovery
                    xmpp.register_plugin('xep_0199') # XMPP Ping
                    xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
                    xmpp.register_plugin('xep_0096') # Jabber Search
                    xmpp.connect()
                    xmpp.process(forever=False)
               except KeyboardInterrupt as e:
                    print('Conversacion finalizada')
                    xmpp.disconnect()

          elif(op2 == "5"):

               try:
                    gr = input("Escriba el JID del grupo: ") 
                    nom = input("Escriba su alias en el grupo: ")
                    if '@conference.alumchat.xyz' in gr:
                         xmpp = Grupo(usu, psd, gr, nom)
                         xmpp.register_plugin('xep_0030')
                         xmpp.register_plugin('xep_0045')
                         xmpp.register_plugin('xep_0199')
                         xmpp.connect()
                         xmpp.process(forever=False)
               except KeyboardInterrupt as e:
                    print('Chat Grupal Finalizado')
                    xmpp.disconnect()
                    

          elif(op2 == "6"):
               msg = input("indique su mensaje de presencia: ") 
               xmpp = Roster(usu, psd, show=False, message=msg)
               xmpp.register_plugin('xep_0030') # Service Discovery
               xmpp.register_plugin('xep_0199') # XMPP Ping
               xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
               xmpp.register_plugin('xep_0096') # Jabber Search
               xmpp.connect()
               xmpp.process(forever=False)

          elif(op2 == "7"):
               para = input("Indique el usuario al que quiere enviar: ") 
               file = input("Direccion del archivo: ") 
               xmpp = Archivos(usu, psd, para, file)
               xmpp.register_plugin('xep_0030') # Service Discovery
               xmpp.register_plugin('xep_0065') # SOCKS5 Bytestreams
               xmpp.connect()
               xmpp.process(forever=False)


          elif(op2 == "8"):
               
               try:
                    
                    para = input("Ingrese el recipiente: ") 
                    msg = input("Mensaje: ")
                    ty = input("Type: ")
                    xmpp = Noti(usu, psd, para, msg, ty)
                    xmpp.register_plugin('xep_0030') # Service Discovery
                    xmpp.register_plugin('xep_0199') # XMPP Ping
                    xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
                    xmpp.register_plugin('xep_0096') # Jabber Search
                    xmpp.connect()
                    xmpp.process(forever=False)
               except KeyboardInterrupt as e:
                    print('Notificaciones finalizadas')
                    xmpp.disconnect()

          elif(op2 == "9"):
               
               xmpp = Del(usu, psd)
               xmpp.register_plugin('xep_0030') # Service Discovery
               xmpp.register_plugin('xep_0004') # Data forms
               xmpp.register_plugin('xep_0066') # Out-of-band Data
               xmpp.register_plugin('xep_0077') # In-band Registration
               xmpp.connect()
               xmpp.process()
               xmpp = None
               control = False
               break


          else:
               print("Opcion invalida intente denuevo")


          print("")
          print("-----------------------------------------------")
          print("Presione 1 para mostrar contactos")
          print("Presione 2 para agregar contactos")
          print("Presione 3 para mostrar detalles de un contacto")
          print("Presione 4 para entrar a un chat 1 a 1")
          print("Presione 5 para entrar a un chat grupal")
          print("Presione 6 para cambiar mensaje de presencia")
          print("Presione 7 para enviar y recibir archivos")
          print("Presione 8 para notificaciones")
          print("Presione 9 para eliminar cuenta")
          print("Presione 10 para cerrar sesion")
          print("-----------------------------------------------")
          print("")
          

          op2  = input("")
          
     print("")
     print("======================================================")
     print("BIENVENIDO AL CHAT")
     print("PRESIONE 1 PARA INGRESAR EN EL SERVIDOR DE ALUMCHAT")
     print("PRESIONE 2 PARA REGISTRARSE EN EL SERVIDOR DE ALUMCHAT")
     print("PRESIONE 3 PARA SALIR")
     print("")
     op = input("Opcion: ")
     print("======================================================")
     print("")
     print("")
     print("")

print("GRACIAS HASTA LUEGO")
        
