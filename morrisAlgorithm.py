# class morrisClass():
# 	"""docstring for morris"""
# 	def __init__(self, counters = 0):
# 		self.counters = counters

# 	@classmethod
# 	def updateCounter(self):
# 		if random.uniform(0,1) < 1.0/(2**self.counters):
# 			self.counters += 1
# 			return self.counters

# 	def getEstimate(self):
# 		return int(2**self.counters - 1)

# class morrisPlusClass():
# 	def __init__(self, mpLoops, morrisPlusTotal = 0):
# 		self.morrisPlusTotal = morrisPlusTotal
# 		self.mpLoops = mpLoops

# 	def morrisPlus(self):
# 		instMorris = morrisClass()
# 		for mpLoop in range(self.mpLoops):
# 			self.morrisPlusTotal += instMorris.getEstimate()
# 		return int(self.morrisPlusTotal/self.mpLoops)

# class morrisPlusPlusClass():
# 	"""docstring for morrisPlusPlus"""
# 	def __init__(self, failureProbability, allowableError, morrisPlusValues = 0):
# 		#mppLoops is number of times morris++ function runs.
# 		self.mppLoops = int(math.log(1/failureProbability))
# 		#mpLoops is number of times morris+ function runs.
# 		self.mpLoops = int(1/float(allowableError**2))

# 		self.morrisPlusValues = [0]*self.mppLoops

# 	def morrisPlusPlus(self):
# 		instMorrisPlus = morrisPlusClass(self.mpLoops)
# 		for mppLoop in range(self.mppLoops):
# 			self.morrisPlusValues[mppLoop] = instMorrisPlus.morrisPlus()
# 		return statistics.median(self.morrisPlusValues)	

# def morrisPlusPlus(counters, mppLoops):
# 	for mppLoop in xrange(mppLoops):
# 		if random.uniform(0,1) < 1.0/(2**counters[mppLoop]):
# 			counters[mppLoop] += 1
# 	values = [2**counters[mppLoop] - 1 for mppLoop in xrange(mppLoops)]
# 	return int(1/float(mppLoops)*sum(values)) 


import random, math, sys, statistics
from multiprocessing import Process

class morrisClass(object):
	def __init__(self, mpLoops, counters):
		self.mpLoops = mpLoops
		self.counters = counters

	def morris(self, mpLoop):
		if random.uniform(0,1) < 1.0/(2**self.counters[mpLoop]):
			return True

	def morrisPlus(self):
		for mpLoop in range(self.mpLoops):
			if self.morris(mpLoop) == True:
				self.counters[mpLoop] = self.counters[mpLoop] + 1
		values = [2**self.counters[mpLoop] - 1 for mpLoop in range(self.mpLoops)]
		meanValues = statistics.mean(values)
		#t(meanValues)
		return meanValues

def morrisPlusPlus(mppLoops, mpLoops, counters, morrisPlusValues):
	#morrisPlusValues = [morrisClass(mpLoops, counters).morrisPlus() for mppLoop in range(mppLoops)]
	for mppLoop in range(mppLoops):
		morrisInstance = morrisClass(mpLoops, counters)
		morrisPlusValues[mppLoop] = morrisInstance.morrisPlus()/(mppLoop+1.5)
		#print(morrisPlusValues[mppLoop], mppLoop)
	return statistics.median(morrisPlusValues)


def main():
	#gets the user defined input using sys library argv 
	streamFile= sys.argv[1]
	allowableError = float(sys.argv[2])
	failureProbability = float(sys.argv[3])
	#check if howOften argument was declared by user
	if len(sys.argv) == 5:
		howOften = float(sys.argv[4].strip("[]"))  # get rid of [] from argument value
	else:
		howOften = 1

	#initialize number of events, current time, new report time
	numEvents = 0
	currentTime = 0
	nextReportTime = howOften

	#mppLoops is number of times morris++ function runs.
	mppLoops = int(math.log(1/failureProbability))
	#mpLoops is number of times morris+ function runs.
	mpLoops = int(1/(2*(allowableError*allowableError)*(1/3)))
	counters = [0]*mpLoops
	morrisPlusValues = [0]*mppLoops

	print(mppLoops, mpLoops)
	print("elapsed time 	exact count 	Morris++ count")
	#read events files and stream each event line into program
	with open("%s"%streamFile, 'r') as fp:
		for line in fp:
			numEvents += 1
			currentTime += float(line)
			morrisValue = morrisPlusPlus(mppLoops, mpLoops, counters, morrisPlusValues)
			if currentTime >= nextReportTime:
				print(str(int(currentTime)) + "		" +
					str(numEvents) +  "		" +
					str(int(morrisValue)))
				nextReportTime += howOften

if __name__ == "__main__":
    main()