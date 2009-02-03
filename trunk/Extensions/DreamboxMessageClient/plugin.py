# -*- coding: utf-8 -*-
from Plugins.Plugin import PluginDescriptor

from DMC import DMC
from DMCSetup import DMCSetup

my_global_session = None
dmc = None

def main(session):
	global dmc
	#dmc = DMC(session)
	session.open(DMCSetup, dmc)

def autostart(reason, **kwargs):
	global dmc
	
	# ouch, this is a hack	
	if kwargs.has_key("session"):
		global my_global_session
		my_global_session = kwargs["session"]
		#return
	
	print "[DreamboxMessageClient] - Autostart"
	global dmc
	if reason == 0:
		dmc = DMC(my_global_session)
	elif reason == 1:
		dmc.shutdown()
		dmc = None

#def Plugins(**kwargs):
	#name = "DbInfo"
	#descr = "Zeigt Verspätungen oder Zugausfälle der DB"
	#return [ PluginDescriptor(name=name, description=descr, where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main) ]

def Plugins(**kwargs):
	name = "DMC"
	descr = "DreamboxMessageClient - Listens to messages from DreamboxMessageServer"
 	return [ PluginDescriptor(name=name, description=descr, where = PluginDescriptor.WHERE_PLUGINMENU, fnc=main), 
		PluginDescriptor(where = [PluginDescriptor.WHERE_SESSIONSTART, PluginDescriptor.WHERE_AUTOSTART], fnc=autostart) ]
