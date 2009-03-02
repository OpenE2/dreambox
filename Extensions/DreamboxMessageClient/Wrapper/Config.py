class Config:
	def __init__(self):
		self.plugins = Plugins()
	
class Plugins:
	def __init__(self):
		self.DMC = DMC()
	
class DMC:
	def __init__(self):
		self.enable = O(True)
		#self.host = O('localhost')
		#self.url = O('http://localhost:8180/dms/DreamboxMessageServer?action=receiver')
		self.host = O('open-dreambox.org')
		self.url = O('http://open-dreambox.org/dms/DreamboxMessageServer?action=receiver')
		self.port = O(8184)
		self.password = O('asdf')
		self.timeout = O(60)
		self.notify_state = O(True)

class O:
	def __init__(self, value):
		self.value = value

config = Config()
