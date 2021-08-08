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
