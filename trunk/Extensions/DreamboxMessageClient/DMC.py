from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.web.client import getPage

from Wrapper.Message import *
from Wrapper.Config import config

from datetime import datetime
import socket
import urllib2
import exceptions
#from urllib import urlopen

my_session = None

class DMProtocol(LineReceiver):
	def connectionMade(self):
		self.sendLine(config.plugins.DMC.password.value)
		debug_log("password sent")
	
	def lineReceived(self, line):
		print "receive:", line
	
		a = line.split(';')
		(action, text) = a[0:2]
		
		if action == "message":
			message(text.replace("\\n","\n"), 60)
			self.sendLine("OK")
		elif action == "question":
			question(my_session, self.questionCallback, text.replace("\\n","\n"), 60, a[2:])
		else:
			self.sendLine("unknown action: " + action)
	
	def questionCallback(self, answer):
		self.sendLine("OK")
		if answer is None:
			self.sendLine("abort")
		else:
			self.sendLine(answer[1])


class DMCFactory(ReconnectingClientFactory):
	initialDelay = 20
	maxDelay = 500
	
	def __init__(self):
		self.hangup_ok = False

	def startedConnecting(self, connector):
		if config.plugins.DMC.notify_state.value:
			message("Connecting to DreamboxMessageServer...", 2)
	
	def buildProtocol(self, addr):
		if config.plugins.DMC.notify_state.value:
			message("Connected to DreamboxMessageServer!", 4)
		self.resetDelay()
		return DMProtocol()
	
	def clientConnectionLost(self, connector, reason):
		if config.plugins.DMC.notify_state.value and not self.hangup_ok:
			message("Connection to DreamboxMessageServer! lost\n (%s)\nretrying..." % reason.getErrorMessage(), config.plugins.DMC.timeout.value)
		ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
	
	def clientConnectionFailed(self, connector, reason):
		if config.plugins.DMC.notify_state.value:
			message("Connecting to DreamboxMessageServer failed\n (%s)\nretrying..." % reason.getErrorMessage(), config.plugins.DMC.timeout.value)
		ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

class DMC:
	def __init__(self, session):
		global my_session
		my_session = session
		self.d = None
		self.connect()
		
	def connect(self):
		if config.plugins.DMC.enable.value:
			url = config.plugins.DMC.url.value
			
			# timeout in seconds
			timeout = 2
			socket.setdefaulttimeout(timeout)
	
			try:
				# this call to urllib2.urlopen now uses the default timeout
				# we have set in the socket module
				req = urllib2.Request(url)
				urlcon = urllib2.urlopen(req)
				port = int(urlcon.read().strip())
			except exceptions.Exception:
				if config.plugins.DMC.notify_state.value:
					message("DMC: Failed to access servlet -> reading port from config", 4)
				port = config.plugins.DMC.port.value
			
			self.connectToHost(config.plugins.DMC.host.value, port)
	
	def connectToHost(self, host, port):
		self.abort()
		
		self.host = host
		self.port = port
		
		f = DMCFactory()
		debug_log(self.host, self.port)
		self.d = (f, reactor.connectTCP(self.host, self.port, f))
	
	def shutdown(self):
		self.abort()
	
	def abort(self):
		if self.d is not None:
			self.d[0].hangup_ok = True 
			self.d[0].stopTrying()
			self.d[1].disconnect()
			self.d = None
