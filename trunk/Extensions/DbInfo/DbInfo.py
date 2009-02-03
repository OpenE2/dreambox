from urllib import urlopen
from datetime import datetime
#from twisted.web.client import getPage
#import time
import re

from DbUserConf import *

spaceSeqPattern = re.compile(' +')

def debug_log(*params):
	print "DEBUG: ", params
	#pass

class DbTrainEvent:
	def __init__(self, urlcon):
		self.train = spaceSeqPattern.sub(' ',  urlcon.readline().strip().replace("<b>",  "").replace("</b>",  ""))
		urlcon.readline()
		self.direction = urlcon.readline().strip()
		urlcon.readline()
		self.time = urlcon.readline().strip().replace("<b>",  "").replace("</b>",  "")
		self.greenInfo = []
		self.redInfo = []
		self.inTime = False
		line = urlcon.readline().strip()
		while (line.startswith('<span class=')):
			if (line.startswith('<span class="red">')):
				self.redInfo.append( line[18:len(line)-7] )
			if (line.startswith('<span class="green">')):
				self.greenInfo.append( line[20:len(line)-7] )
			if (line.find('p&#252;nktl.') >= 0):
				self.inTime = True
			line = urlcon.readline().strip()
		if not (line.startswith("Gl.")):
			line = urlcon.readline().strip()
		self.track = line[4:len(line) - 6]
		debug_log(self.train, self.direction, self.time, self.greenInfo, self.redInfo, self.track, self.inTime)

class DbData:
	def __init__(self, url):
		urlcon = urlopen(url)
		try:
			# find station and time info
			while 1:
				line = urlcon.readline().strip()
				if (line == '<p class="sqdetails">'):
					self.station = urlcon.readline().strip().replace("<b>",  "").replace("</b><br />",  "")
					line = urlcon.readline().strip()
					parts = line.split(' ')
					self.direction = parts[0]
					self.time = parts[1]
					line = urlcon.readline().strip()
					parts = line.split(' ')
					self.date = parts[1]
					debug_log(self.station, self.direction, self.time, self.date)
					break;
			self.trainEvents = []
			while line:
				line = urlcon.readline().strip()
				if (line == '<p class="sqdetailsDep">'):
					self.trainEvents.append(DbTrainEvent(urlcon))
#		except IOError as (errno, strerror):
#			print "I/O error({0}): {1}".format(errno, strerror)
#		except ValueError:
#			print "Could not convert data to an integer."
		except:
			print "Unexpected error:"
			raise
		urlcon.close()



class DbInfo:
	#def __init__(self):
		#self.phonebook = {}
		#self.reload()
	def _gotPage(self, data):
		print "[FritzProtocol] _gotPage"
		#try:
			#self.gotPage(data)
		#except:
			#import traceback, sys
			#traceback.print_exc(file=sys.stdout)
			##raise e
			#self.handleEvent()

	def handleEventOnError(self, error):
		print "[FritzProtocol] handleEventOnError - Error :%s" %error
		self.handleEvent()

	def handleEvent(self):
		print "[FritzProtocol] handleEvent!"

	def getDbData(self,  stationId):
		""" Returns the current info from mobile.bahn.de as DbData. """
		d = datetime.now()
		time = str(d.hour) + ":" + str(d.minute)
		url = "http://localhost/dbextension/data2.html"
		url = "http://mobile.bahn.de/bin/mobil/bhftafel.exe/dox?si=" + stationId + "&bt=dep&ti=" + time + "&p=1111101&max=100&mode=actual&start=yes"
		return DbData(url)

def main(session):
	s = ""
	for station in stations:
		s += station.alias + "\n"
		ext = DbInfo()
		dbData = ext.getDbData(station.stationId)
		
		for i in dbData.trainEvents:
			for trainFilter in station.trainFilter:
				if (trainFilter[0].match(i.train) and trainFilter[1].match(i.direction)):
					info = ""
					if i.inTime:
						info = "OK "
					if i.redInfo:
						info += " ".join(i.redInfo)
					s += "  " + i.time + "  " + info + "\n"
					break
	return s
