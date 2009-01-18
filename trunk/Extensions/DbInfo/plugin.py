# -*- coding: utf-8 -*-
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox

from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.config import config, ConfigSubsection, ConfigSelection, ConfigIP, ConfigEnableDisable, getConfigListEntry, ConfigText, ConfigInteger
from Components.ConfigList import ConfigListScreen

from Plugins.Plugin import PluginDescriptor
from Tools import Notifications

import DbInfo

Session = None

def main(session, servicelist, **kwargs):
	global Session
	Session = session
	text = DbInfo.main(session)
	Notifications.AddNotification(MessageBox, text, type=MessageBox.TYPE_INFO, timeout=60)

#def autostart(reason, **kwargs):
	#global fritz_call
	
	## ouch, this is a hack	
	#if kwargs.has_key("session"):
		#global my_global_session
		#my_global_session = kwargs["session"]
		#return
	
	#print "[Fritz!Call] - Autostart"
	#if reason == 0:
		#fritz_call = FritzCall()
	#elif reason == 1:
		#fritz_call.shutdown()
		#fritz_call = None

def Plugins(**kwargs):
	name = "DbInfo"
	descr = "Zeigt Verspätungen oder Zugausfälle der DB"
	return [ PluginDescriptor(name=name, description=descr, where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main) ]

#def Plugins(**kwargs):
 	#return [ PluginDescriptor(name="FritzCall", description="Display Fritzbox-Fon calls on screen", where = PluginDescriptor.WHERE_PLUGINMENU, fnc=main), 
		#PluginDescriptor(where = [PluginDescriptor.WHERE_SESSIONSTART, PluginDescriptor.WHERE_AUTOSTART], fnc = autostart) ]
