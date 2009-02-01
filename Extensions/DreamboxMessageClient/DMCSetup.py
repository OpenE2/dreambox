from Screens.Screen import Screen
from Screens.MessageBox import MessageBox

from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.config import config, ConfigSubsection, ConfigSelection, ConfigIP, ConfigEnableDisable, getConfigListEntry, ConfigText, ConfigInteger
from Components.ConfigList import ConfigListScreen

from Wrapper.Config import config

class DMCSetup(ConfigListScreen, Screen):
	skin = """
		<screen position="100,90" size="550,420" title="DMC Setup" >
		<widget name="config" position="20,10" size="510,300" scrollbarMode="showOnDemand" />
		<widget name="consideration" position="20,320" font="Regular;20" halign="center" size="510,50" />
		</screen>"""

	def __init__(self, session, dmc, args = None):
		
		Screen.__init__(self, session)
		
		self.dmc = dmc
		
		self["consideration"] = Label(_("You need a stable internet connection to use this plugin!"))
		self.list = []
		
		self["setupActions"] = ActionMap(["SetupActions"], 
		{
			"save": self.save, 
			"cancel": self.cancel, 
			"ok": self.save, 
		}, -2)

		ConfigListScreen.__init__(self, self.list)
		self.createSetup()

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.createSetup()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.createSetup()

	def createSetup(self):
		self.list = [ ]
		self.list.append(getConfigListEntry(_("Enable DMC"), config.plugins.DMC.enable))
		if config.plugins.DMC.enable.value:
			self.list.append(getConfigListEntry(_("Hostname"), config.plugins.DMC.host))
			self.list.append(getConfigListEntry(_("Port"), config.plugins.DMC.port))
			self.list.append(getConfigListEntry(_("URL"), config.plugins.DMC.url))
			self.list.append(getConfigListEntry(_("Password"), config.plugins.DMC.password))
			self.list.append(getConfigListEntry(_("Timeout"), config.plugins.DMC.timeout))
			self.list.append(getConfigListEntry(_("Notify about state changes"), config.plugins.DMC.notify_state))
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)

	def save(self):
		print "[DMCSetup] save"
		for x in self["config"].list:
			x[1].save()
		if self.dmc is not None:
			self.dmc.connect()
		
		self.close()

	def cancel(self):
		print "[DMCSetup] cancel"
		for x in self["config"].list:
			x[1].cancel()
		self.close()
