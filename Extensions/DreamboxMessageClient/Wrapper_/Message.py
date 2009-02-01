from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Tools import Notifications

def debug_log(*params):
	pass

def message(text, timeout):
	Notifications.AddNotification(MessageBox, text, type=MessageBox.TYPE_INFO, timeout=timeout)

def error(text, timeout):
	print "error: " + text

def question(session, callback, text, timeout, answers):
	list = map(lambda x: (x,x), answers)
	keys = range(1, min(len(answers)+1, 10))
	session.openWithCallback(callback, ChoiceBox, title=text, list=list, keys=keys)
	#keys = []
	#list = []
	#for x in self.availableKeys:
		#if self.extensionKeys.has_key(x):
			#entry = self.extensionKeys[x]
			#extension = self.extensionsList[entry]
			#if extension[2]():
				#name = str(extension[0]())
				#list.append((extension[0](), extension))
				#keys.append(x)
				#extensionsList.remove(extension)
			#else:
				#extensionsList.remove(extension)
	#for x in extensionsList:
		#list.append((x[0](), x))
	#keys += [""] * len(extensionsList)
