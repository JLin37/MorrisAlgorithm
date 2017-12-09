#!/usr/bin/python
#============================================================================
# 	Morris Approximate Counting of Events
#
#	Give a periodic approximation of the number of events in an input stream.
#	Each event is represented by the amount of time (in seconds) since the 
#	previous event.
#	Our output displays the time elapsed at each periodic output of 
#	exact count and approximation count
#
#	Work Distribution:
#	Menghao Lin: Wrote the python program to run the morris Algorithm by
#	reading the events file.
#	Ziqi Wang:
#	Xinliang Zhong:
#
#	Authors: Menghao Lin (Jason), Xinliang Zhong, Ziqi Wang
#	Date: 10 Dec 2017
#	
#============================================================================

import random, math, sys

def morrisPlusPlus(counters, mppLoops):
	for mppLoop in xrange(mppLoops):
		if random.uniform(0,1) < 1.0/(2**counters[mppLoop]):
			counters[mppLoop] += 1
	values = [2**counters[mppLoop] - 1 for mppLoop in xrange(mppLoops)]
	return int(1/float(mppLoops)*sum(values)) 

def main():
	streamFile= sys.argv[1]
	allowableError = float(sys.argv[2])
	failureProbability = float(sys.argv[3])
	#check if howOften argument was declared by user
	if len(sys.argv) == 5:
		howOften = float(sys.argv[4].strip("[]"))  # get rid of [] from argument value
	else:
		howOften = 1

	print(streamFile, allowableError, failureProbability, howOften)
	numEvents = 0
	currentTime = 0
	nextReportTime = howOften
	#mppLoops is number of times morris++ function runs
	mppLoops = int(1/float(allowableError**2)*math.log(1/failureProbability))
	counters = [0]*mppLoops

	with open("%s"%streamFile, 'r') as fp:
	#with open(streamFile, 'r') as fp:
		for line in fp:
			numEvents += 1
			currentTime += float(line)
			morrisValue = morrisPlusPlus(counters, mppLoops)
			if currentTime >= nextReportTime:
				print(str(currentTime) + 
					" actual count: " + str(numEvents) + 
					" morris estimate: " + str(morrisValue))

if __name__ == "__main__":
    main()