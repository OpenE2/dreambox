def debug_log(*params):
	print "DEBUG: ", params
	#pass

def message(text, timeout):
	print "message: " + text

def error(text, timeout):
	print "error: " + text

def question(session, callback, text, timeout, answers):
	print "question: " + text, answers
	callback((answers[0], answers[0]))
