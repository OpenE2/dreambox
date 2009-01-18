import re

class DbStation:
	def __init__(self, alias, stationId, trainFilter):
		self.alias = alias
		self.stationId = stationId
		self.trainFilter = []
		for i in trainFilter:
			self.trainFilter.append((re.compile(i[0]), re.compile(i[1])))
